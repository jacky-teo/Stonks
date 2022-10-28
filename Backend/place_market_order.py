from flask import Flask, request, jsonify
from flask_cors import CORS  # enable CORS
import ast

import requests, json # for api requests
from functions import url, getRecord # tbank gateway endpoint

from placeMarketOrder import placeMarketOrder
from getCustomerStocks import getStockSymbols

# importing utilities
from get_ending_shares_no import get_ending_shares_no
from get_no_of_shares_to_purchase import get_no_of_shares_to_purchase
from get_total_value_of_fund_portfolio import get_total_value_of_fund_portfolio
from get_all_fund_portfolio import get_all_fund_portfolio

app = Flask(__name__)

@app.route("/rebalance", methods=['POST'])
def rebalance():
    if request.is_json:
        json_details = request.get_json()

        # print(json_details)

        additional_invest = float(json_details["additionalInvest"])
        allocation = ast.literal_eval(json_details["allocation"])
        price = ast.literal_eval(json_details["price"])
        current_shares = ast.literal_eval(json_details["currentShares"])
        print("My current portfolio:", current_shares)
        userID = json_details["userID"]
        PIN = json_details["PIN"]
        settlementAccount = json_details["settlement_account"]
        OTP = json_details["OTP"] if "OTP" in json_details else 999999

        message = process_rebalance(additional_invest, allocation, price, current_shares, userID, PIN, settlementAccount, OTP)

        return jsonify(
        {
            "code": 200,
            "message": message
        }
    ), 200

def process_rebalance(additional_invest, allocation, price, current_shares, userID, PIN, settlementAccount, OTP='999999'):
    # get_ending_shares_no + get_current_shares > get_no_of_shares_to_purchase > 
    #   if positive number (buy) > placemarketorder (buy)
    #   if negative number (sell) > placemarketorder (sell)
    # give JSON response from tBank
    response = "Nothing happened"

    fund_stocks = list(allocation.keys())

    fund_portfolio = get_all_fund_portfolio(userID, PIN, OTP, fund_stocks)
    print("Fund Portfolio:", fund_portfolio)
    inital_invest = get_total_value_of_fund_portfolio(fund_portfolio)
    total_invest = additional_invest + inital_invest

    ending_shares = get_ending_shares_no(total_invest, allocation, price)
    print("Ending Share:", ending_shares)
    qty_purchase = get_no_of_shares_to_purchase(ending_shares, current_shares)

    if qty_purchase:
        for symbol in qty_purchase:
            quantity = qty_purchase[symbol]

            if quantity > 0:
                buyOrSell = 'buy'
                response = placeMarketOrder(userID, PIN, settlementAccount, buyOrSell, symbol, quantity, OTP)
            elif quantity < 0:
                buyOrSell = 'sell'
                quantity *= -1
                response = placeMarketOrder(userID, PIN, settlementAccount, buyOrSell, symbol, quantity, OTP)
            else:
                continue

    return response

# ====================

# tBank Functions

    # getCustomerStocks(): Get all stocks owned by customer (including 0 quantity)

# ====================
def getCustomerStocks(userID, PIN, OTP):
    #Header
    serviceName = 'getCustomerStocks'
    
    headerObj = {
                        'Header': {
                        'serviceName': serviceName,
                        'userID': userID,
                        'PIN': PIN,
                        'OTP':OTP
                        }
                        }
    
    final_url="{0}?Header={1}".format(url(),json.dumps(headerObj))
    response = requests.post(final_url)
    serviceRespHeader = response.json()['Content']['ServiceResponse']['ServiceRespHeader']
    errorCode = serviceRespHeader['GlobalErrorID']

    customer_portfolio = {}

    if errorCode == '010000':
        depository_list = response.json()['Content']['ServiceResponse']['DepositoryList']
        if depository_list == {}:
            print("No record found!")
        else:
            depository_list = depository_list['Depository']
            recordCount = getRecord(depository_list)
            if recordCount > 1:
                for i in range(0,recordCount,1):
                    depository = depository_list[i]
                    symbol_company = getStockSymbols(depository['symbol'])
                    # print("\nSymbol Name: {}".format(symbol_company))
                    # print("Quantity: {}".format(depository['quantity']))
                    # print("Price: {}".format(depository['price']))
                    # print("Trading Date: {}".format(depository['tradingDate']))
                    # print("Customer ID: {}".format(depository['customerID']))
                    
                    customer_portfolio[depository['symbol']] = {
                        'company': symbol_company,
                        'quantity': depository['quantity'],
                        'price': depository['price'],
                        'trading_date': depository['tradingDate'],
                        'customer_id': depository['customerID']
                    }

            elif recordCount == 0:
                    symbol_company = getStockSymbols(depository_list['symbol'])
                    # print("\nSymbol Name: {}".format(symbol_company))
                    # print("Quantity: {}".format(depository_list['quantity']))
                    # print("Price: {}".format(depository_list['price']))
                    # print("Trading Date: {}".format(depository_list['tradingDate']))
                    # print("Customer ID: {}".format(depository_list['customerID']))

                    customer_portfolio[depository['symbol']] = {
                        'company': symbol_company,
                        'quantity': depository_list['quantity'],
                        'price': depository_list['price'],
                        'trading_date': depository_list['tradingDate'],
                        'customer_id': depository_list['customerID']
                    }

    elif errorCode == '010041':
        print("OTP has expired.\nYou will receiving a SMS")
    else:
        print(serviceRespHeader['ErrorText'])

    return customer_portfolio

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010, debug=True)