from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS  # enable CORS

app = Flask(__name__)
cors =CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/stonks'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Transactions(db.Model):
    __tablename__ = 'transactions'
# (`transaction_id`, `user_id`,`marketplace_id`, `stock_symbol`,`stock_price`,`volume`,`date`)
    transaction_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    marketplace_id = db.Column(db.Integer, nullable=False)
    stock_symbol = db.Column(db.String(50), nullable=False)
    transaction_quantity = db.Column(db.Integer, nullable=False)
    stock_priice = db.Column(db.Float(precision=2), nullable=False)
    volume = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    def __init__(self, transaction_id, user_id, marketplace_id,stock_symbol, transaction_quantity, stock_price, volume, date):
        self.transaction_id = transaction_id
        self.user_id = user_id
        self.marketplace_id = marketplace_id
        self.stock_symbol = stock_symbol
        self.transaction_quantity = transaction_quantity
        self.stock_price = stock_price
        self.volume = volume
        self.date = date
    
    def json(self):
        return {"transaction_id": self.transaction_id, "user_id": self.user_id, "marketplace_id":self.marketplace_id,"stock_symbol": self.stock_symbol, "transaction_quantity": self.transaction_quantity, "stock_price": self.stock_price, "volume": self.volume, "date": self.date}

#--Get all Transactions--#
@app.route("/transactions")
def get_all():
    transactionList = Transactions.query.all()
    if len(transactionList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "transactions": [transaction.json() for transaction in transactionList]
                }
            }
        ),200
    return jsonify(
        {
            "code": 404,
            "message": "There are no transactions."
        }
    ), 404

## get all transactions by userid
@app.route("/transactions/user/<int:user_id>")
def find_by_user_id(user_id):
    transaction = Transactions.query.filter_by(user_id=user_id)
    if transaction:
        return jsonify(
            {
                "code": 200,
                "data": transaction.json()
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "Transaction not found."
        }
    ), 404

## add new transaction
@app.route("/transactions/add", methods=['POST'])
def create_transaction():
    data = request.get_json()
    transaction = Transactions(**data)

    try:
        db.session.add(transaction)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "transaction_id": transaction.transaction_id
                },
                "message": "An error occurred creating the transaction."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": transaction.json()
        }
    ), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)