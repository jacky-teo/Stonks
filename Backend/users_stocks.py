from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS  # enable CORS
from users import Users
from stocks import Stocks
from funds_stocks import FundsStocks
from users_funds   import UsersFunds
from getCustomerStocks import getCustomerStocks
from getStockPrice import getStockPrice
from getStockSymbols import getStockSymbols
from marketplace_stocks import MarketplaceStocks
app = Flask(__name__)
cors =CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/stonks'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


### update Stonks Database
@app.route("/updateStonksDB/<int:user_id>")
def updateStonksDB(user_id):
    user_info = Users.query.filter_by(user_id=user_id).first()
    stocksList = Stocks.query.all()
    if user_info:
        user_stocks = getCustomerStocks(userID = user_info.user_acc_id,PIN = user_info.user_pin)
        stockListSymbols = []
        ## get all stockListSybols
        for stock in stocksList:
            stockListSymbols.append(stock.stock_symbol)
        ### Add stock to tBank Database
        for us in user_stocks['Depository']:
            if us['symbol'] not in stockListSymbols:
                stock_details = {
                    'stock_symbol':us['symbol'],
                }
                stock_information = getStockPrice(stock_details['stock_symbol'])
                print(stock_information)
                stock_details['stock_name'] = stock_information['company']
                stock = Stocks(stock_symbol=stock_details['stock_symbol'],stock_name=stock_details['stock_name'])
                try:
                    db.session.add(stock)
                    db.session.commit()
                    return jsonify({"code": 200, "data": stock_details}), 200
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
            "code": 200,
            "message": "There are no stocks."
        }
    ), 200
        

# tBank Functions
# --- Get all stocks not owned 
@app.route("/not_owned_stocks/tbank/<int:user_id>")
def get_stocks_by_not_owned_customer_id(user_id):
    user_info = Users.query.filter_by(user_id=user_id).first()
    stocksList = Stocks.query.all()
    result = []

    if user_info:
        user_stocks = getCustomerStocks(userID = user_info.user_acc_id,PIN = user_info.user_pin)
        usList = []

        for us in user_stocks['Depository']:
            print(us)
            #Check if symbol in stonks database
            stock = Stocks.query.filter_by(stock_symbol=us['symbol']).first()
            stock_id = len(stocksList)+1
            if stock is None:
                # Add stock to marketplacestocks
                
                # Add stock to stonks database

                # Get Stock Details
                stock_details = getStockPrice(us['symbol'])
                print(stock_details['company'])
                new_stock = Stocks(stock_id = stock_id,stock_symbol = us['symbol'],stock_name = stock_details['company'])
                db.session.add(new_stock)
                db.session.commit()

                
                marketplace_stocks = MarketplaceStocks(1,stock_id,1000000)
                db.session.add(marketplace_stocks)
                db.session.commit()

        for us in user_stocks['Depository']:
            usList.append(us['symbol'])
        for stock in stocksList:
            if stock.stock_symbol not in usList:
            
                stock_price = getStockPrice(symbol=stock.stock_symbol)
                
                if stock_price:
                    stock_price = stock_price['Price']
                else:
                    stock_price="No data"

                stock_details = {
                    'stock_id':stock.stock_id,
                    'stock_symbol':stock.stock_symbol,
                    'stock_name':stock.stock_name,
                    "stock_price": stock_price
                }
                result.append(stock_details)
        return jsonify(
            {
                "code": 200,
                "data": {
                    "stocks": [stocks for stocks in result]
                }
            }
        ),200
    return jsonify(
        {
            "code": 404,
            "message": "There are no stocks."
        }
    ), 404
    
# tBank Functions
#Get Stocks Owned By User In tBank via getCustomerStocks.py
@app.route("/users_stocks/tbank/<int:user_id>")
def find_by_user_id_tbank(user_id):
    user_info = Users.query.filter_by(user_id=user_id).first()
    usersFundsList = UsersFunds.query.filter_by(user_id=user_id).all()
    fundIDList = [fund.fund_id for fund in usersFundsList]
    stockIDList = []
    stocksList = Stocks.query.all()

    # Get customer stocks from tBank
    if user_info:
        user_stocks = getCustomerStocks(userID = user_info.user_acc_id,PIN = user_info.user_pin)


        for id in fundIDList:
            stockInFund = FundsStocks.query.filter_by(fund_id=id).all()

            for sID in stockInFund:
                if sID.stock_id not in stockIDList:
                    stockIDList.append(sID.stock_id)

        

                



        mappedStocks = []
        for s in stocksList:
            for id in stockIDList:
                if s.stock_id == id:
                    mappedStocks.append(s.stock_symbol)

        print(mappedStocks)
        if user_stocks:

            stocks = []
            for x in user_stocks['Depository']:
                if x['symbol'] in mappedStocks:
                    p = {
                        "customerID": x['customerID'],
                        "price": x['price'],
                        "quantity": x['quantity'],
                        "symbol": x['symbol'],
                        "mapped": True,
                        "company": getStockSymbols(x['symbol']),
                        "tradingDate": x['tradingDate']
                    } 
                    stocks.append(p)
                else:
                    p = {
                        "customerID": x['customerID'],
                        "price": x['price'],
                        "quantity": x['quantity'],
                        "symbol": x['symbol'],
                        "mapped": False,
                        "company": getStockSymbols(x['symbol']),
                        "tradingDate": x['tradingDate']
                    } 
                    stocks.append(p)


            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "user_stocks": [
                            # users for users in user_stocks['Depository']
                            stocks
                            ]
                    }
                }
            ),200
        return jsonify(
            {
                "code": 404,
                "message": "There are no stocks for this user."
            }
        ), 404

## Stocks not mapped to funds_stocks
@app.route("/not_mapped_stocks/<int:user_id>")
def get_stocks_by_not_mapped_customer_id(user_id):
    
    user_info = Users.query.filter_by(user_id=user_id).first()
    usersFundsList = UsersFunds.query.filter_by(user_id=user_id).all()
    fundIDList = [fund.fund_id for fund in usersFundsList]
    stockIDList = []
    stocksList = Stocks.query.all()
    
    if user_info:
        user_stocks = getCustomerStocks(userID = user_info.user_acc_id,PIN = user_info.user_pin)



    for id in fundIDList:
        stockInFund = FundsStocks.query.filter_by(fund_id=id).all()
        for sID in stockInFund:
            if sID.stock_id not in stockIDList:
                stockIDList.append(sID.stock_id)
    

    mappedStocks = []
    for s in stocksList:
        for id in stockIDList:
            if s.stock_id == id:
                mappedStocks.append(s.stock_id)

    unmappedStocks = []
    for s in stocksList:
        if s.stock_id not in mappedStocks:
            unmappedStocks.append(s)
    if len(unmappedStocks) > 0:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "stocks": [stocks.json() for stocks in unmappedStocks]
                }
            }
        ),200
    else:
        return jsonify(
            {
                "code": 404,
                "message": "There are no stocks."
            }
        ), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)