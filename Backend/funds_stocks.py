from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS  # enable CORS
from stocks import Stocks
from getCustomerStocks import getCustomerStocks
from getStockPrice import getStockPrice
from getStockHistory import getStockHistory
from users import Users
from funds import Funds

app = Flask(__name__)
cors =CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/stonks'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class FundsStocks(db.Model):
    __tablename__ = 'funds_stocks'

    fund_id = db.Column(db.Integer, primary_key=True)
    stock_id = db.Column(db.Integer, primary_key=True)
    allocation = db.Column(db.Float(precision=2), nullable=False)
    def __init__(self, fund_id, stock_id, allocation):
        self.fund_id = fund_id
        self.stock_id = stock_id
        self.allocation = allocation
    
    def json(self):
        return {"fund_id": self.fund_id, "stock_id": self.stock_id, "allocation": self.allocation}


## Get current allocation of stocks in a fund ##
@app.route("/current_funds_stocks/<int:fund_id>/<int:user_id>")
def get_current_funds_stocks(fund_id,user_id):
    fundsStocksList = db.session.query(FundsStocks.stock_id, FundsStocks.allocation)\
        .filter(FundsStocks.fund_id == fund_id)\
        .join(Stocks, FundsStocks.stock_id == Stocks.stock_id)\
        .join(Funds, FundsStocks.fund_id == Funds.fund_id)\
        .add_columns(Stocks.stock_symbol,Funds.fund_investment_amount)\
        .all()

    user_info = Users.query.filter_by(user_id=user_id).first()
    user_stocks = getCustomerStocks(userID = user_info.user_acc_id,PIN = user_info.user_pin)['Depository']
    print(user_stocks)
    currentFundList = []
    total_investment=0
    for us in user_stocks:
        currentFund = {}
        for stock in fundsStocksList:
            if stock[2] == us['symbol']:
                total_investment += int(us['quantity'])*float(getStockPrice(us['symbol'])['Price'])

    for us in user_stocks:
        currentFund = {}
        for stock in fundsStocksList:
            if stock[2] == us['symbol']:
                currentFund['symbol'] = us['symbol']
                currentFund['volume'] = us['quantity']

                currentFund['price'] = getStockPrice(us['symbol'])['Price']
                currentFund['stock_name'] = getStockPrice(us['symbol'])['company']
                allocation = int(us['quantity'])*float(getStockPrice(us['symbol'])['Price'])/total_investment
                currentFund['allocation_value'] =  int(us['quantity'])*float(getStockPrice(us['symbol'])['Price'])
                currentFund['allocation'] = round(allocation,2)
                currentFundList.append(currentFund)
    
    

    if len(fundsStocksList):
        return jsonify(
            {
                "code": 200,
                "data":currentFundList
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "There are no funds in the database."
        }
    ), 404

#--Get all Funds settlement id--#
@app.route("/funds_stocks")
def get_all():
    fundStocks = FundsStocks.query.all()
    if len(fundStocks):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "fundsSettlement": [fundStock.json() for fundStock in fundStocks]
                }
            }
        ),200
    return jsonify(
        {
            "code": 404,
            "message": "There are no stocks settled."
        }
    ), 404

#--Get all Funds settlement id--#
@app.route("/a_fund_stocks/<int:fund_id>")
def get_fund_stocks(fund_id):
    fundStocks = FundsStocks.query.filter_by(fund_id=fund_id).all()
    if len(fundStocks):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "allocation": [fundStock.json() for fundStock in fundStocks]
                }
            }
        ),200
    return jsonify(
        {
            "code": 404,
            "message": "There are no stocks in fund."
        }
    ), 404

## add a new fund settlement id
@app.route("/funds_stocks/add", methods=['POST'])
def create_fund_settlement():
    data = request.get_json()
    print(data)
    fundSettlement = FundsStocks(**data)
    try:
        db.session.add(fundSettlement)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "fund_id": fundSettlement.fund_id,
                    "stock_id": fundSettlement.stock_id
                },
                "message": "An error occurred while creating the fund settlement."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": fundSettlement.json()
        }
    ), 201

#get stocks by fund_id 
@app.route("/fund_stocks/user/<int:fund_id>/<int:user_id>")
def get_stocks_by_fund_id(fund_id,user_id):
    fundStocks = db.session.query(FundsStocks.fund_id, FundsStocks.allocation)\
        .filter(FundsStocks.fund_id == fund_id)\
        .join(Stocks, FundsStocks.stock_id == Stocks.stock_id)\
        .add_columns(Stocks.stock_symbol, Stocks.stock_name)

    results = []
    for fundStock in fundStocks:
        results.append({
            "fund_id": fundStock[0],
            "stock_symbol": fundStock[2],
            "stock_name": fundStock[3],
            "allocation": fundStock[1],
    })
    if (fundStocks):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "fundsSettlement": [result for result in results]
                }
            }
    ),200 
    return jsonify(
        {
            "code": 404,
            "message": "There are no stocks in fund."
        }
    ), 404

# Drop all current allocations and update with new allocations
@app.route("/funds_stocks/update_allocation", methods=['POST'])
def update_stocks_allocation():
    data = request.get_json()
    allocations = data["allocations"]
    fund_id = data["fund_id"]
    new_funds_stocks = [FundsStocks(fund_id, allocation["stock_id"], allocation["allocation"]) for allocation in allocations]

    # Drops all fund_stock records
    FundsStocks.query.filter_by(fund_id=fund_id).delete()

    # Commits all new fund_stock records
    try:
        db.session.add_all(new_funds_stocks)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "funds_stocks": [fund_stock.json() for fund_stock in new_funds_stocks]
                },
                "message": "An error occurred while creating the skills_courses."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": {
                "funds_stocks": [fund_stock.json() for fund_stock in new_funds_stocks]
            }
        }
    ), 201

@app.route("/fund_stocks/stock_history/<fund_id>/<user_id>/<pin>")
def get_stock_history(fund_id,user_id, pin):

    fundStocks = db.session.query(FundsStocks.fund_id)\
        .filter(FundsStocks.fund_id == fund_id)\
        .join(Stocks, FundsStocks.stock_id == Stocks.stock_id)\
        .add_columns(Stocks.stock_symbol)
    fund_stocks = {}
    for stock in fundStocks:
        fund_stocks.update(getStockHistory(userID = user_id,PIN = pin, symbol=stock.stock_symbol, numDays='30'))

    if len(fund_stocks):

        return jsonify(
            {
                "code": 200,
                "data": fund_stocks
            }
        ),200
    return jsonify(
        {
            "code": 404,
            "message": "There are no such stocks."
        }
    ), 404
@app.errorhandler(404) 
def invalid_route(e): 
    return "Invalid route."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)