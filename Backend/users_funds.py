from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS  # enable CORS
app = Flask(__name__)
cors =CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/stonks'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from stocks import Stocks
from funds import Funds

db = SQLAlchemy(app)

class UsersFunds(db.Model):
    __tablename__ = 'users_funds'

    user_id = db.Column(db.Integer, primary_key=True)
    fund_id = db.Column(db.Integer, primary_key=True)

    def __init__(self, user_id, fund_id):
        self.user_id = user_id
        self.fund_id = fund_id
    
    def json(self):
        return {"user_id": self.user_id, "fund_id": self.fund_id}


## Get Funds By User ID ##
@app.route("/funds/user_funds/<int:user_id>")
def get_funds_by_user_id(user_id):
    fundsList = db.session.query(UsersFunds.fund_id)\
        .filter(UsersFunds.user_id == user_id)\
        .join(Funds, UsersFunds.fund_id == Funds.fund_id)\
        .add_columns(Funds.fund_name)\
        .add_columns(Funds.fund_goals)\
        .add_columns(Funds.fund_investment_amount)\
        .all()
    
    if len(fundsList):
        return jsonify(
            {
                "code": 200,
                "data":[
                    {
                        "fund_id":fund[0], 
                        "fund_name":fund[1],
                        "fund_goals":fund[2],
                        "fund_investment_amount":fund[3],
                        
                    } for fund in fundsList
                ]
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "User funds not found."
        }
    ), 404

#--Get all Users Funds--#
@app.route("/users_funds")
def get_all():
    usersFundsList = UsersFunds.query.all()
    print(usersFundsList)
    if len(usersFundsList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "users_funds": [users_funds.json() for users_funds in usersFundsList]
                }
            }
        ),200
    return jsonify(
        {
            "code": 404,
            "message": "There are no users funds."
        }
    ), 404

#--Get all Users Funds by user_id--#
@app.route("/users_funds/user/<int:user_id>")
def find_by_user_id(user_id):
    usersFundsList = UsersFunds.query.filter_by(user_id=user_id).all()
    if usersFundsList:
        return jsonify(
            {
                "code": 200,
                "data": [users_funds.json() for users_funds in usersFundsList]
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "Users funds not found."
        }
    ), 404

##-- add a new user fund --##
@app.route("/users_funds/add", methods=['POST'])
def create_user_fund():
    data = request.get_json()
    user_id = data['user_id']
    fund_id = data['fund_id']

    if (UsersFunds.query.filter_by(user_id=user_id, fund_id=fund_id).first()):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "user_id": user_id,
                    "fund_id": fund_id
                },
                "message": "User fund already exists."
            }
        ), 400

    user_fund = UsersFunds(user_id, fund_id)
    
    try:
        db.session.add(user_fund)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "user_id": user_id,
                    "fund_id": fund_id
                },
                "message": "An error occurred while creating the user fund."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": user_fund.json()
        }
    ), 201



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006, debug=True)