from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS  # enable CORS

app = Flask(__name__)
cors =CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/stonks'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class MarketplaceStocks(db.Model):
    __tablename__ = 'marketplace_stocks'
    marketplace_id = db.Column(db.Integer, primary_key=True)
    stock_id=db.Column(db.Integer,primary_key=True)
    volume_in_market=db.Column(db.Integer, nullable=False)

    def __init__(self, marketplace_id, stock_id, volume_in_market):
        self.marketplace_id = marketplace_id
        self.stock_id = stock_id
        self.volume_in_market = volume_in_market
    
    def json(self):
        return {"marketplace_id": self.marketplace_id, "stock_symbol": self.stock_id, "volume_in_marketplace": self.volume_in_market}

#--Get all Marketplace Stocks--#
@app.route("/marketplace_stocks")
def get_all():
    marketplaceStocksList = MarketplaceStocks.query.all()
    if len(marketplaceStocksList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "marketplace_stocks": [marketplaceStocks.json() for marketplaceStocks in marketplaceStocksList]
                }
            }
        ),200
    return jsonify(
        {
            "code": 404,
            "message": "There are no marketplace stocks."
        }
    ), 404

# --Get Marketplce Stocks by Symbol and Marketplace ID--#
@app.route("/marketplace_stocks/<int:stock_id>/<int:marketplace_id>")
def find_by_stock_symbol_and_marketplace_id(stock_id, marketplace_id):
    marketplaceStocksList = MarketplaceStocks.query.filter_by(stock_id=stock_id, marketplace_id=marketplace_id).all()
    if marketplaceStocksList:
        return jsonify(
            {
                "code": 200,
                "data": [marketplaceStocks.json() for marketplaceStocks in marketplaceStocksList]
            }
        ),200
    return jsonify(
        {
            "code": 404,
            "message": "Marketplace Stocks not found."
        }
    ), 404

#--volume volume in marketplace and stock symbol--#
@app.route("/marketplace_stocks/transaction/<int:stock_id>/<int:marketplace_id>", methods=['PUT'])
def update_marketplace_stocks(stock_id, marketplace_id):
    marketplaceStocks = MarketplaceStocks.query.filter_by(stock_id=stock_id, marketplace_id=marketplace_id)
    if marketplaceStocks:
        data = request.get_json()
        if data['transaction_type'] == "buy":
            marketplaceStocks.volume_in_marketplace += data['transaction_volume']
        elif data['transaction_type'] == "sell":
            marketplaceStocks.volume_in_marketplace -= data['transaction_volume']
        try:
            db.session.commit()
        except:
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "marketplace_stocks": marketplaceStocks.json()
                    },
                    "message": "An error occurred while updating the marketplace stocks."
                }
            ), 500

        return jsonify(
            {
                "code": 200,
                "data": marketplaceStocks.json()
            }
        ),200

    return jsonify(
        {
            "code": 404,
            "message": "Marketplace Stocks not found."
        }
    ), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5008, debug=True)