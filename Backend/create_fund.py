from asyncio.windows_events import NULL
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS
from sqlalchemy import null  # enable CORS
from users import Users
from getCustomerStocks import getCustomerStocks
from getStockPrice import getStockPrice
from getStockSymbols import getStockSymbols
from invokes import invoke_http


app = Flask(__name__)
cors =CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/stonks'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route("/create-fund", methods=['POST'])
def create_fund():
    FUND_BASE_URL = "http://localhost:5000"
    FUNDS_USERS_STOCKS_BASE_URL = "http://localhost:5002"

    data = request.get_json()

    newFundDetails = {
        "fund_name" : data["fund_name"],
        "fund_goal" : data["fund_goal"],
        "fund_initial_value" : data["fund_initial_value"],
        "fund_interval" : data["fund_interval"],
    }


    # Get the fund name, initial value, fund interval -> funds -> return Fund ID
    newFund = invoke_http(FUND_BASE_URL+"/funds/add",method="POST",json=newFundDetails)

    # Get the fund_id, user_id, stock name, stock symbol, allocation -> funds_users_stocks
    fundUserStockDetails = {
        "fund_id" : newFund.data.fund_id,
        "user_stock_id" : null,
        "allocation" : data["allocation"],
    }
    
    fundUserStocks = invoke_http(FUNDS_USERS_STOCKS_BASE_URL+"/funds_users_stocks/add",method="POST",json=fundUserStockDetails)
    # Get the user id



    return None


#Get Stocks Owned By User In tBank via getCustomerStocks.py
@app.route("/common/stockprice/<int:user_id>/<string:symbol>")
def getStockPrice_tbank(user_id, symbol):
    
    user_info = Users.query.filter_by(user_id=user_id).first()
    if user_info:
        stock_details = getStockPrice(userID = user_info.user_acc_id,PIN = user_info.user_pin, symbol=symbol)

        if stock_details:
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "stock_details": stock_details
                    }
                }
            ),200
        return jsonify(
            {
                "code": 404,
                "message": "There is no stock price for this symbol."
            }
        ), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)