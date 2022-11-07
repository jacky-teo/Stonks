from datetime import date
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from funds_stocks import FundsStocks
from stocks import Stocks
from getCustomerStocks import getCustomerStocks
from getStockPrice import getStockPrice
from getStockHistory import getStockHistory
from users import Users
from funds import Funds
from os import environ
from flask_cors import CORS  # enable CORS
import sys
sys.path.append("../")

app = Flask(__name__)
cors =CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/stonks'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


    
# @app.route("/fund_stocks/stock_history/<int:user_id>/<int:fund_id>")
# def get_stocks_history(user_id, fund_id):
#     print('running')
    
#     fundStocks = FundsStocks.query.filter_by(fund_id=fund_id)
#     user_info = Users.query.filter_by(user_id=user_id).first()
#     user_stocks = getCustomerStocks(userID = user_info.user_acc_id,PIN = user_info.user_pin)['Depository']
#     print(user_stocks)
#     results =[]

#     if fundStocks:
#         for fundStock in fundStocks:
#             stock = Stocks.query.filter_by(stock_id=fundStock.stock_id).first()
#             fund = Funds.query.filter_by(fund_id=fund_id).first()
#             for us in user_stocks:
#                 price = getStockPrice(userID = user_info.user_acc_id,PIN = user_info.user_pin,symbol=us['symbol'] )['Price']
#                 if us['symbol'] == stock.stock_symbol:
#                     results.append({
#                         "fund_id": fund.fund_id,
#                         "fund_name": fund.fund_name,
#                         "stock_id": stock.stock_id,
#                         "stock_symbol": us['symbol'],
#                         "stock_name": stock.stock_name,
#                         "stock_price": price,
#                         "allocation": fundStock.allocation,
#                         "volume": us['quantity']
#                     })
    
#     test = []
#     for stock in results:
#         print(stock.stock_name)
#         print(stock.stock_symbol)
#         p = {
#             "stock_name": stock.stock_name,
#             "stock_history": getStockHistory(userID = user_info.user_acc_id,PIN = user_info.user_pin, symbol=stock.stock_symbol, numDays='30')
#         }
#         test.append(p)
#     if len(test):
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": {
#                     "stocks": results
#                 }
#             }
#         ),200
#     return jsonify(
#         {
#             "code": 404,
#             "message": "There are no such stocks."
#         }
#     ), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5011, debug=True)