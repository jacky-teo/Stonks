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

class UsersStocks(db.Model):
    __tablename__ = 'users_stocks'

    user_stock_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    stock_id = db.Column(db.Integer, nullable=False)
    stock_price = db.Column(db.Float(precision=2), nullable=False)
    volume = db.Column(db.Integer, nullable=False)
    
    def __init__(self, user_stock_id, user_id, stock_id, stock_price, volume):
        self.user_stock_id = user_stock_id
        self.user_id = user_id
        self.stock_id = stock_id
        self.stock_price = stock_price
        self.volume = volume
    
    def json(self):
        return {"user_stock_id": self.user_stock_id, "user_id": self.user_id, "stock_symbol": self.stock_id, "stock_price": self.stock_price, "volume": self.volume}

#--Get all Settlements--#
@app.route("/users_stocks")
def get_all():
    users_stocksList = UsersStocks.query.all()
    if len(users_stocksList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "users_stocks": [users_stocks.json() for users_stocks in users_stocksList]
                }
            }
        ),200
    return jsonify(
        {
            "code": 404,
            "message": "There are no users stocks."
        }
    ), 404

#get all settlement by userid
@app.route("/users_stocks/user/<int:user_id>")
def find_by_user_id(user_id):
    users_stocksList = UsersStocks.query.filter_by(user_id=user_id)
    if users_stocksList:
        return jsonify(
            {
                "code": 200,
                "data":[users_stocks.json() for users_stocks in users_stocksList]
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "There are no stocks for this user."
        }
    ), 404

#-- Get a Settlement --#
@app.route("/users_stocks/<int:user_stock_id>")
def find_by_settlement_id(user_stock_id):
    settlement = UsersStocks.query.filter_by(user_stock_id=user_stock_id).first()
    if settlement:
        return jsonify(
            {
                "code": 200,
                "data": settlement.json()
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "There are no funds for this user."
        }
    ), 404

#Update a stock price
@app.route("/users_stocks/stockprice/<int:user_stock_id>", methods=['PUT'])
def update_stock_price(user_stock_id):
    settlement = UsersStocks.query.filter_by(user_stock_id=user_stock_id).first()
    if settlement:
        data = request.get_json()
        settlement.stock_price = data['stock_price']
        try:
            db.session.commit()
        except:
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "settlement_id": settlement.settlement_id
                    },
                    "message": "An error occurred updating the stock price."
                }
            ), 500

        return jsonify(
            {
                "code": 200,
                "data": settlement.json()
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "Settlement not found."
        }
    ), 404

#-- Update Settlement volume and price--#
@app.route("/users_stocks/volume/<int:user_stock_id>", methods=['PUT'])
def update_settlement(user_stock_id):
    settlement = UsersStocks.query.filter_by(user_stock_id=user_stock_id).first()
    if settlement:
        data = request.get_json()
        settlement.volume = data['volume']
        settlement.stock_price = data['stock_price']
        try:
            db.session.commit()
        except:
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "settlement_id": settlement.settlement_id
                    },
                    "message": "An error occurred updating the settlement."
                }
            ), 500

        return jsonify(
            {
                "code": 200,
                "data": settlement.json()
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "Settlement not found."
        }
    ), 404

#Get Stocks Owned By User In tBank via getCustomerStocks.py
@app.route("/users_stocks/tbank/<int:user_id>")
def find_by_user_id_tbank(user_id):
    
    user_info = Users.query.filter_by(user_id=user_id).first()
    if user_info:
        user_stocks = getCustomerStocks(userID = user_info.user_acc_id,PIN = user_info.user_pin)
        if user_stocks:
            stocks = []
            for x in user_stocks['Depository']:
                p = {
                    "customerID": x['customerID'],
                    "price": x['price'],
                    "quantity": x['quantity'],
                    "symbol": x['symbol'],
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
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)