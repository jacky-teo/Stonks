from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS  # enable CORS
import sys
sys.path.append("../")


app = Flask(__name__)
cors =CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/stonks'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Funds(db.Model):
    __tablename__ = 'funds'

    fund_id = db.Column(db.String(24), primary_key=True)
    fund_name = db.Column(db.String(64), nullable=False)
    fund_goals = db.Column(db.Float(precision=2),nullable=False)
    fund_investment_amount = db.Column(db.Float(precision=2),nullable=False)

    def __init__(self, fund_id, fund_name, fund_goals, fund_investment_amount):
        self.fund_id = fund_id
        self.fund_name = fund_name
        self.fund_goals = fund_goals
        self.fund_investment_amount = fund_investment_amount

    def json(self):
        return {"fund_id": self.fund_id, "fund_name": self.fund_name, "fund_goals": self.fund_goals, "fund_investment_amount": self.fund_investment_amount}

#--Get all Funds--#
@app.route("/funds")
def get_all():
    fundsList = Funds.query.all()
    if len(fundsList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "funds": [fund.json() for fund in fundsList]
                }
            }
        ),200
    return jsonify(
        {
            "code": 404,
            "message": "There are no funds."
        }
    ), 404

#-- Get a Fund --#
@app.route("/funds/<int:fund_id>")
def find_by_fund_id(fund_id):
    fund = Funds.query.filter_by(fund_id=fund_id).first()
    if fund:
        return jsonify(
            {
                "code": 200,
                "data": fund.json()
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "Fund not found."
        }
    ), 404

## -- Add a Fund --##
@app.route("/funds/add", methods=['POST'])
def create_fund():
    data = request.get_json()
    fund = Funds(**data)

    try:
        db.session.add(fund)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "fund_id": fund.fund_id
                },
                "message": "An error occurred while creating the fund."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": fund.json()
        }
    ), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)