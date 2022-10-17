from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS  # enable CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/stonks'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class FundsSettlement(db.Model):
    __tablename__ = 'funds_settlement'

    fund_id = db.Column(db.Integer, primary_key=True)
    settlement_id = db.Column(db.Integer, nullable=False)
   
    def __init__(self, fund_id, settlement_id):
        self.fund_id = fund_id
        self.settlement_id = settlement_id
    
    def json(self):
        return {"fund_id": self.fund_id, "settlement_id": self.settlement_id}

#--Get all Funds settlement id--#
@app.route("/funds_settlement")
def get_all():
    fundsSettlementList = FundsSettlement.query.all()
    if len(fundsSettlementList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "fundsSettlement": [fundSettlement.json() for fundSettlement in fundsSettlementList]
                }
            }
        ),200
    return jsonify(
        {
            "code": 404,
            "message": "There are no stocks settled."
        }
    ), 404

#-- Get a Fund settlement id --#
@app.route("/funds_settlement/<int:fund_id>")
def find_by_fund_id(fund_id):
    fundSettlement = FundsSettlement.query.filter_by(fund_id=fund_id)
    if fundSettlement:
        return jsonify(
            {
                "code": 200,
                "data": fundSettlement.json()
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "Fund settlement not found."
        }
    ), 404

## add a new fund settlement id
@app.route("/funds_settlement", methods=['POST'])
def create_fund_settlement():
    data = request.get_json()
    fundSettlement = FundsSettlement(**data)
    try:
        db.session.add(fundSettlement)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "fund_id": fundSettlement.fund_id,
                    "settlement_id": fundSettlement.settlement_id
                },
                "message": "An error occurred while creating the fund settlement."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": fundSettlement.json()
        }
    ), 201