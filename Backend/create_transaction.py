'''

Function will take in the following parameters:
    - user_id                [String]
    - stock_symbol           [String]
    - quantity               [String]
    - price                  [String]
    - datetime               [String]
Parameters will be achieved from process_rebalance endpoint in place_market_order.py

'''
from transactions import Transactions
from marketplace_stocks import MarketplaceStocks
from datetime import datetime
from stocks import Stocks

from users import Users
from flask import jsonify
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # enable CORS

app = Flask(__name__)
cors =CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/stonks'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


def process_transaction(userID,stock_symbol,volume,price):
    # Get stock_id from stock_symbol
    stock_id = Stocks.query.filter_by(stock_symbol=stock_symbol).first().stock_id
    # Get volume of stocks in marketplace_stocks
    # Get User_id from users
    user_id = Users.query.filter_by(user_acc_id=userID).first().user_id
    date = datetime.now()
    # Create a transaction
    transaction = Transactions(None,user_id, 1,stock_id, price[stock_symbol],volume,date)
    print(transaction.json())
    db.session.add(transaction)
    db.session.commit()

    
def update_marketplace(stock_symbol,volume):
    stock_id = Stocks.query.filter_by(stock_symbol=stock_symbol).first().stock_id
    marketplaceStocks = MarketplaceStocks.query.filter_by(stock_id=stock_id).first()
    newVol =  marketplaceStocks.market_vol+volume
    marketplaceStocks.market_vol = newVol
    print(marketplaceStocks.json())
    db.session.flush()


    



