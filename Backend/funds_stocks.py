from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS  # enable CORS
from stocks import Stocks
from getCustomerStocks import   getCustomerStocks
from getStockPrice import getStockPrice
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
    fundStocks = FundsStocks.query.filter_by(fund_id=fund_id)
    user_info = Users.query.filter_by(user_id=user_id).first()
    user_stocks = getCustomerStocks(userID = user_info.user_acc_id,PIN = user_info.user_pin)['Depository']
    print(user_stocks)
    results =[]

    if fundStocks:
        for fundStock in fundStocks:
            stock = Stocks.query.filter_by(stock_id=fundStock.stock_id).first()
            fund = Funds.query.filter_by(fund_id=fund_id).first()
            for us in user_stocks:
                price = getStockPrice(userID = user_info.user_acc_id,PIN = user_info.user_pin,symbol=us['symbol'] )['Price']
                if us['symbol'] == stock.stock_symbol:
                    results.append({
                        "fund_id": fund.fund_id,
                        "fund_name": fund.fund_name,
                        "stock_id": stock.stock_id,
                        "stock_symbol": us['symbol'],
                        "stock_name": stock.stock_name,
                        "stock_price": price,
                        "allocation": fundStock.allocation,
                        "volume": us['quantity']
                    })
    print(results)
    return jsonify(
        {
            "code": 200,
            "data": {
                "fundsSettlement": [fundStock for fundStock in results]
            }
        }
    ),200   



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)