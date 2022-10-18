from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS  # enable CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/stonks'
db = SQLAlchemy(app)

class MarketPlace(db.Model):
    __tablename__ = 'market_place'
    
    stock_symbol=db.Column(db.String(50), nullable=False)
    volume = db.Column(db.Integer, nullable=False)
    
    def __init__(self, stock_symbol, volume):
        self.stock_symbol = stock_symbol
        self.volume = volume
    
    def json(self):
        return {"stock_symbol": self.stock_symbol, "volume": self.volume}

#--Get all MarketPlace--#
@app.route("/market_place")
def get_all():
    marketPlaceList = MarketPlace.query.all()
    if len(marketPlaceList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "market_place": [market_place.json() for market_place in marketPlaceList]
                }
            }
        ),200
    return jsonify(
        {
            "code": 404,
            "message": "There are no market_place."
        }
    ), 404

#get volume by symbol
@app.route("/market_place/<string:stock_symbol>")
def find_by_stock_symbol(stock_symbol):
    market_place = MarketPlace.query.filter_by(stock_symbol=stock_symbol)
    if market_place:
        return jsonify(
            {
                "code": 200,
                "data": market_place.json()
            }
        ),200
    return jsonify(
        {
            "code": 404,
            "message": "Market Place not found."
        }
    ), 404