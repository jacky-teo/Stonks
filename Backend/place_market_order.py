from flask import Flask, request, jsonify
from flask_cors import CORS  # enable CORS
import ast

from placeMarketOrder import placeMarketOrder
from getStockPrice import getStockPrice

# importing utilities
from get_ending_shares_no import get_ending_shares_no
from get_no_of_shares_to_purchase import get_no_of_shares_to_purchase
from get_total_value_of_fund_portfolio import get_total_value_of_fund_portfolio
from get_all_fund_portfolio import get_all_fund_portfolio

app = Flask(__name__)

@app.route("/rebalance", methods=['POST'])
def rebalance():
    # tBank APIs used
        # getStockPrice
        # getCustomerStocks
        # placeMarketOrder

    if request.is_json:
        json_details = request.get_json()

        additional_invest = float(json_details["additionalInvest"])         # Additional investments
        allocation = ast.literal_eval(json_details["allocation"])           # Fund stocks allocations

        # Get all price for fund_stocks
        fund_stocks = list(allocation.keys())
        price = {}
        for ticker in fund_stocks:
            price[ticker] = float(getStockPrice(ticker)["Price"])
        
        userID = json_details["userID"]
        PIN = json_details["PIN"]
        settlementAccount = json_details["settlement_account"]
        OTP = json_details["OTP"] if "OTP" in json_details else 999999

        message = process_rebalance(additional_invest, allocation, price, userID, PIN, settlementAccount, OTP)

        return jsonify(
        {
            "code": 200,
            "message": message
        }
    ), 200

def process_rebalance(additional_invest, allocation, price, userID, PIN, settlementAccount, OTP='999999'):
    # get_ending_shares_no + get_current_shares > get_no_of_shares_to_purchase > 
    #   if positive number (buy) > placemarketorder (buy)
    #   if negative number (sell) > placemarketorder (sell)
    # give JSON response from tBank
    response_dict = {}

    fund_stocks = list(allocation.keys())

    fund_portfolio = get_all_fund_portfolio(userID, PIN, OTP, fund_stocks)
    # print("Fund Portfolio:", fund_portfolio)
    inital_invest = get_total_value_of_fund_portfolio(fund_portfolio, price)
    total_invest = additional_invest + inital_invest

    ending_shares = get_ending_shares_no(total_invest, allocation, price)
    # print("Ending Share:", ending_shares)
    qty_purchase = get_no_of_shares_to_purchase(ending_shares, fund_portfolio)

    if qty_purchase:
        for symbol in qty_purchase:
            quantity = qty_purchase[symbol]
            response = ""

            if quantity > 0:
                buyOrSell = 'buy'
                response = placeMarketOrder(userID, PIN, settlementAccount, buyOrSell, symbol, quantity, OTP)
            elif quantity < 0:
                buyOrSell = 'sell'
                quantity *= -1
                response = placeMarketOrder(userID, PIN, settlementAccount, buyOrSell, symbol, quantity, OTP)
            else:
                continue

            response_dict[symbol] = {
                "response": response
            }
    
    # Output Statement - for debugging purpose
    print("User Details:", userID, PIN, settlementAccount, OTP)
    print("\n Fund Details:", allocation)
    print("Current prices for the fund stocks:", price)
    print("\n Current Fund Portfolio:", fund_portfolio)
    print("\n Initial + Additional Investment: ", inital_invest, "+" , additional_invest, "=", total_invest)
    print("\n Ending Fund Portfolio:", ending_shares)
    print("\n How much to purchase to reach end:", qty_purchase)
    print("Response:", response_dict)

    return response_dict

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010, debug=True)