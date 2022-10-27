from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS  # enable CORS
import sys
sys.path.append("../")
from stocks import Stocks
from funds_users_stocks import FundsUsersStocks
from users_stocks import UsersStocks
from users_funds import UsersFunds

import requests, json # for api requests
from functions import url # tbank gateway endpoint

app = Flask(__name__)
cors =CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/stonks'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Funds(db.Model):
    __tablename__ = 'funds'

    fund_id = db.Column(db.String(24), primary_key=True)
    fund_name = db.Column(db.String(64), nullable=False)
    fund_goals = db.Column(db.Float(precision=2),nullable=False)
    fund_investment_amount = db.Column(db.Float(precision=2),nullable=False)

    def __init__(self, fund_id, fund_name, fund_goals, fund_investment_amount):
        self.fund_id = fund_id
        self.fund_name = fund_name
        self.fund_goals = fund_goals
        self.fund_investment_amount = fund_investment_amount

    def json(self):
        return {"fund_id": self.fund_id, "fund_name": self.fund_name, "fund_goals": self.fund_goals, "fund_investment_amount": self.fund_investment_amount}

#--Get all Funds--#
@app.route("/funds")
def get_all():
    fundsList = Funds.query.all()
    if len(fundsList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "funds": [fund.json() for fund in fundsList]
                }
            }
        ),200
    return jsonify(
        {
            "code": 404,
            "message": "There are no funds."
        }
    ), 404

#-- Get a Fund --#
@app.route("/funds/<int:fund_id>")
def find_by_fund_id(fund_id):
    fund = Funds.query.filter_by(fund_id=fund_id).first()
    if fund:
        return jsonify(
            {
                "code": 200,
                "data": fund.json()
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "Fund not found."
        }
    ), 404

## -- Add a Fund --##
@app.route("/funds/add", methods=['POST'])
def create_fund():
    data = request.get_json()
    fund = Funds(**data)

    try:
        db.session.add(fund)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "fund_id": fund.fund_id
                },
                "message": "An error occurred while creating the fund."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": fund.json()
        }
    ), 201

## Get Stocks by Fund ID ##
@app.route("/funds/fund_settlement/<int:fund_id>")
def get_stocks_by_fund_id(fund_id):
    fundsSettlementStockList = db.session.query(FundsUsersStocks.fund_id)\
        .filter(FundsUsersStocks.fund_id == fund_id)\
        .join(UsersStocks, FundsUsersStocks.user_stock_id == UsersStocks.user_stock_id)\
        .add_columns(UsersStocks.volume)\
        .join(Stocks, UsersStocks.stock_id == Stocks.stock_id)\
        .add_columns(Stocks.stock_name)\
        .all()
    
    if len(fundsSettlementStockList):
        print("------------------------------" + str(fundsSettlementStockList[0]))
        return jsonify(
            {
                "code": 200,
                "data":[
                    {
                        "fund_id":fundSettlement[0], 
                        "volume":fundSettlement[1], 
                        "stock_name":fundSettlement[2]
                    } for fundSettlement in fundsSettlementStockList
                ]
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "Fund stocks not found."
        }
    ), 404

## Get Funds by User ID ##
@app.route("/funds/user_funds/<int:user_id>")
def get_funds_by_user_id(user_id):
    fundsList = db.session.query(UsersFunds.fund_id)\
        .filter(UsersFunds.user_id == user_id)\
        .join(Funds, UsersFunds.fund_id == Funds.fund_id)\
        .add_columns(Funds.fund_name)\
        .add_columns(Funds.fund_goals)\
        .add_columns(Funds.fund_investment_amount)\
        .all()
    
    if len(fundsList):
        return jsonify(
            {
                "code": 200,
                "data":[
                    {
                        "fund_id":fund[0], 
                        "fund_name":fund[1],
                        "fund_goals":fund[2],
                        "fund_investment_amount":fund[3],
                        
                    } for fund in fundsList
                ]
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "User funds not found."
        }
    ), 404

# Utility Helper Functions
def get_ending_shares_no(total_invest, allocation, price):
    '''
        Takes in the following inputs:
            - Total Fund Investment Amount in SGD                           [Integer]       (e.g. 1000)
            - Stocks (Ticker) with its Allocation Percentage in the fund    [Dictionary]    (e.g. { "GOOG": 0.4, "D05.SI": 0.4, "S68.SI": 0.2 })
            - Price of each Stock in SGD                                    [Dictionary]    (e.g. { "GOOG": 103.485, "D05.SI": 32.76, "S68.SI": 8.35 })
        and outputs:
            - Number of shares to own for each stock                        [Dictionary]    (e.g. { "GOOG": 3, "D05.SI": 12, "S68.SI": 23 })
    '''
    ending_shares = {}

    for ticker in allocation:
        ticker_price = price[ticker]
        ticker_allocation = allocation[ticker]
        dollar_allocated = ticker_allocation * total_invest
        quantity = int(dollar_allocated/ticker_price)
        ending_shares[ticker] = quantity

    return ending_shares

def get_no_of_shares_to_purchase(ending_shares, current_shares):
    '''
        Takes in the following inputs:
                - Quantity of ending stocks each        [Dictionary]    (e.g. { "GOOG": 3, "D05.SI": 12, "S68.SI": 23 })
                - Quantity of current stocks each       [Dictionary]    (e.g. { "GOOG": 2, "D05.SI": 0, "S68.SI": 250 })
            and outputs:
                - Quantity of stocks to purchase each   [Dictionary]    (e.g. { "GOOG": 1, "D05.SI": 12, "S68.SI": -227 })
    '''
    qty_purchase = {}

    for ticker in ending_shares:
        ending = ending_shares[ticker]
        starting = current_shares[ticker]
        to_purchase = ending - starting
        qty_purchase[ticker] = to_purchase

    return qty_purchase

def placeMarketOrder():
    #Header
    serviceName = 'placeMarketOrder'
    userID = 'vasng'
    PIN = '114581'
    OTP = '999999'
    #Content
    settlementAccount = '0000009311'
    symbol = 'TSLA'
    buyOrSell = 'buy'
    quantity = '1'
    
    headerObj = {
        'Header': {
            'serviceName': serviceName,
            'userID': userID,
            'PIN': PIN,
            'OTP': OTP
        }
    }
    contentObj = {
        'Content': {
            'settlementAccount': settlementAccount,
            'symbol': symbol,
            'buyOrSell': buyOrSell,
            'quantity': quantity
        }
    }
    final_url="{0}?Header={1}&Content={2}".format(url(),json.dumps(headerObj),json.dumps(contentObj))
    response = requests.post(final_url)
    serviceRespHeader = response.json()['Content']['ServiceResponse']['ServiceRespHeader']
    errorCode = serviceRespHeader['GlobalErrorID']
    
    if errorCode == '010000':
        marketOrder = response.json()['Content']['ServiceResponse']['StockOrder']
        print("You have successfully placed a market order. The order ID is {}.".format(marketOrder['orderID']))

    elif errorCode == '010041':
        print("OTP has expired.\nYou will receiving a SMS")
    else:
        print(serviceRespHeader['ErrorText'])


def process_rebalance(qty_purchase):
    # get_ending_shares_no + get_current_shares > get_no_of_shares_to_purchase > 
    #   if positive number (buy) > placemarketorder (buy)
    #   if negative number (sell) > placemarketorder (sell)
    # give JSON response from tBank? or custom
    response = "Nothing happened"

    

    return response

# --- Start of testing get_ending_shares_no() ---

total_invest = 1000
allocation = {
    "GOOG": 0.4, 
    "D05.SI": 0.4, 
    "S68.SI": 0.2
}
price = {
    "GOOG": 103.485, 
    "D05.SI": 32.76, 
    "S68.SI": 8.35 
}

ending_shares = get_ending_shares_no(total_invest, allocation, price)
print(ending_shares)

current_shares = {
    "GOOG": 2, 
    "D05.SI": 0, 
    "S68.SI": 250
}
print(get_no_of_shares_to_purchase(ending_shares, current_shares))

# placeMarketOrder()

# --- End of testing get_ending_shares_no() ---

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)