from flask import Flask, request, jsonify
from flask_cors import CORS  # enable CORS
import ast

import requests, json # for api requests
from functions import url, getRecord # tbank gateway endpoint
from getCustomerStocks import getStockSymbols


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

    # placeMarketOrder(): Place market order for buying or selling a single stock on tBank
    # getCustomerStocks(): Get all stocks owned by customer (including 0 quantity)

# ====================
def placeMarketOrder(userID, PIN, settlementAccount, buyOrSell, symbol, quantity, OTP):
    '''
        Takes in the following inputs:
            - userID                [String]
            - PIN                   [String]
            - settlementAccount     [String]
            - buyOrSell             [String]
            - symbol                [String]
            - quantity              [String]
            - OTP                   [String]
        and outputs:
            - None                  [NoneType]
    '''
    #Header
    serviceName = 'placeMarketOrder'
    
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
        return "You have successfully placed a market order. The order ID is {}.".format(marketOrder['orderID'])

    elif errorCode == '010041':
        return "OTP has expired.\nYou will receiving a SMS"
    else:
        return serviceRespHeader['ErrorText']


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

# ====================

# Utility Helper Functions

    # get_ending_shares_no():               Get the ending amount of shares to own depending on allocation & total investment amount
    # get_no_of_shares_to_purchase():       Get the number of shares to purchase each for a fund, based on the ending shares to own and the current shares in the fund
    # get_all_fund_portfolio():             Get all customer stocks details which is in the fund
    # get_total_value_of_fund_portfolio():  Get the total value of the fund portfolio

# ====================


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
        ticker_allocation = float(allocation[ticker])
        dollar_allocated = ticker_allocation * float(total_invest)
        quantity = int(dollar_allocated/ticker_price)
        ending_shares[ticker] = quantity

    print("Ending Shares:", ending_shares)
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
        starting = 0 if ticker not in current_shares else current_shares[ticker]
        to_purchase = ending - starting
        qty_purchase[ticker] = to_purchase

    print("How much to buy:", qty_purchase)
    return qty_purchase


def get_all_fund_portfolio(userID, PIN, OTP, fund_stocks):
    fund_portfolio = {}

    customer_portfolio = getCustomerStocks(userID, PIN, OTP)

    for ticker in customer_portfolio:
        if ticker in fund_stocks:
            fund_portfolio[ticker] = customer_portfolio[ticker]

    return fund_portfolio

def get_total_value_of_fund_portfolio(fund_portfolio):
    total = 0

    for ticker in fund_portfolio:
            price = float(fund_portfolio[ticker]['price'])
            quantity = float(fund_portfolio[ticker]['quantity'])
            total += price * quantity

    return total

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010, debug=True)