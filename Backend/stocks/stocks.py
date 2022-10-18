from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS  # enable CORS

app = Flask(__name__)
cors =CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/stonks'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Stocks(db.Model):
    __tablename__ = 'stocks'
    stock_symbol = db.Column(db.String(50), primary_key=True)
    stock_name = db.Column(db.String(64), nullable=False)


    def __init__(self, stock_symbol, stock_name):
        self.stock_symbol = stock_symbol
        self.stock_name = stock_name
    
    def json(self):
        return {"stock_symbol": self.stock_symbol, "stock_name": self.stock_name}
    
#get all stocks 
@app.route("/stocks")
def get_all():
    stocksList = Stocks.query.all()
    if len(stocksList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "stocks": [stocks.json() for stocks in stocksList]
                }
            }
        ),200
    return jsonify(
        {
            "code": 404,
            "message": "There are no stocks."
        }
    ), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)