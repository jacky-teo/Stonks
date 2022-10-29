from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from getStockPrice import getStockPrice
from users import Users
from os import environ
from flask_cors import CORS  # enable CORS
import sys
sys.path.append("../")

### REFACTORING NEEDED ####
# from users_stocks import UsersStocks
### ------------------ ####

# from funds_stocks import FundsStocks

# from users import Users


app = Flask(__name__)
cors =CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/stonks'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Stocks(db.Model):
    __tablename__ = 'stocks'
    stock_id = db.Column(db.Integer, primary_key=True)
    stock_symbol = db.Column(db.String(50),  nullable=False)
    stock_name = db.Column(db.String(64), nullable=False)


    def __init__(self, stock_id,stock_symbol, stock_name):
        self.stock_id = stock_id
        self.stock_symbol = stock_symbol
        self.stock_name = stock_name
    
    def json(self):
        return {"stock_id": self.stock_id,"stock_symbol": self.stock_symbol, "stock_name": self.stock_name}
    
#get all stocks 
@app.route("/stocks")
def get_all():
    stocksList = Stocks.query.all()
    if len(stocksList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "stocks": [stocks.json() for stocks in stocksList]
                }
            }
        ),200
    return jsonify(
        {
            "code": 404,
            "message": "There are no stocks."
        }
    ), 404

# Add stock
@app.route("/stocks/add", methods=['POST'])
def add_stock():
    data = request.get_json()
    stock_symbol = data['stock_symbol']
    stock_name = data['stock_name']
    stock = Stocks(stock_symbol, stock_name)
    try:
        db.session.add(stock)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "stock_id": stock.stock_id
                },
                "message": "An error occurred while creating the stock."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": stock.json()
        }
    ), 201
    
#get all stocks by user_id 
@app.route("/stocks-with-price/<int:user_id>")
def get_all_with_price(user_id):
    stocksList = Stocks.query.all()
    user_info = Users.query.filter_by(user_id=user_id).first()
    if len(stocksList):
        stocks = []
        for stock in stocksList:
            p = {
                "stock_id": stock.stock_id,
                "stock_symbol": stock.stock_symbol,
                "stock_name": stock.stock_name,
                "stock_price": getStockPrice(userID = user_info.user_acc_id,PIN = user_info.user_pin,symbol=stock.stock_symbol)
            }
            stocks.append(p)

        return jsonify(
            {
                "code": 200,
                "data": {
                    "stocks": stocks
                }
            }
        ),200
    return jsonify(
        {
            "code": 404,
            "message": "There are no stocks."
        }
    ), 404


#### Refactoring Needed ####

#get stocks by fund_id 
# @app.route("/fund_stocks/<int:fund_id>")
# def get_stocks_by_fund_id(fund_id):
#     fundsSettlementStockList = db.session.query(FundsStocks.fund_id)\
#         .filter(FundsStocks.fund_id == fund_id)\
#         .join(UsersStocks, FundsStocks .user_stock_id == UsersStocks.user_stock_id)\
#         .add_columns(UsersStocks.volume)\
#         .join(Stocks, UsersStocks.stock_id == Stocks.stock_id)\
#         .add_columns(Stocks.stock_name)\
#         .all()

#     if len(fundsSettlementStockList):
#         print("------------------------------" + str(fundsSettlementStockList[0]))
#         return jsonify(
#             {
#                 "code": 200,
#                 "data":[
#                     {
#                         "fund_id":fundSettlement[0], 
#                         "volume":fundSettlement[1], 
#                         "stock_name":fundSettlement[2]
#                     } for fundSettlement in fundsSettlementStockList
#                 ]
#             }
#         ), 200
#     return jsonify(
#         {
#             "code": 404,
#             "message": "Fund stocks not found."
#         }
#     ), 404
## ------------------------ ##


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)