from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS  # enable CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/stonks'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Settlement(db.Model):
    __tablename__ = 'settlement'

    settlement_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    stock_symbol=db.Column(db.String(50), nullable=False)
    stock_price =db.Cloumn(db.Float(precision=2), nullable=False)
    volumne = db.Column(db.Float(precision=2), nullable=False)
    
    def __init__(self, settlement_id, user_id, stock_id, stock_price, volume):
        self.settlement_id = settlement_id
        self.user_id = user_id
        self.stock_id = stock_id
        self.stock_price = stock_price
        self.volume = volume
    
    def json(self):
        return {"settlement_id": self.settlement_id, "user_id": self.user_id, "stock_id": self.stock_id, "stock_price": self.stock_price, "volume": self.volume}

#--Get all Settlements--#
@app.route("/settlements")
def get_all():
    settlementList = Settlement.query.all()
    if len(settlementList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "settlements": [settlement.json() for settlement in settlementList]
                }
            }
        ),200
    return jsonify(
        {
            "code": 404,
            "message": "There are no settlements."
        }
    ), 404

#get all settlement by userid
@app.route("/settlements/<int:user_id>")
def find_by_user_id(user_id):
    settlement = Settlement.query.filter_by(user_id=user_id)
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

#-- Get a Settlement --#
@app.route("/settlements/<int:settlement_id>")
def find_by_settlement_id(settlement_id):
    settlement = Settlement.query.filter_by(settlement_id=settlement_id).first()
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
@app.route("/settlements/<int:settlement_id>", methods=['PUT'])
def update_stock_price(settlement_id):
    settlement = Settlement.query.filter_by(settlement_id=settlement_id).first()
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
@app.route("/settlements/<int:settlement_id>", methods=['PUT'])
def update_settlement(settlement_id):
    settlement = Settlement.query.filter_by(settlement_id=settlement_id).first()
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)