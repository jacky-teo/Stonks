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
from getStockPrice import getStockPrice
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

    
def update_marketplace(stock_symbol,volume):
    stock_id = Stocks.query.filter_by(stock_symbol=stock_symbol).first().stock_id
    stock_details = getStockPrice(stock_symbol)
    print('details: ',stock_details)
    # stock_vol = stock_details['Volume']
    marketplaceVolume = MarketplaceStocks.query.filter_by(stock_id=stock_id).first().vol
    print('marketplaceVolume: ',marketplaceVolume)
    newVol = marketplaceVolume - volume
    marketplaceStocks = db.session.query(MarketplaceStocks).filter(MarketplaceStocks.stock_id == stock_id)\
    .update({'vol':newVol})
    print('After Update:', marketplaceStocks)
    db.session.commit()


    



