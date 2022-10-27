from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS  # enable CORS
from users import Users
from getCustomerStocks import getCustomerStocks
from getStockPrice import getStockPrice
from getStockSymbols import getStockSymbols
app = Flask(__name__)
cors =CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/stonks'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


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