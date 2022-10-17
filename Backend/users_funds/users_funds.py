from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS  # enable CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/stonks'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class UsersFunds(db.Model):
    __tablename__ = 'users_funds'

    user_id = db.Column(db.Integer, primary_key=True)
    fund_id = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, fund_id):
        self.user_id = user_id
        self.fund_id = fund_id
    
    def json(self):
        return {"user_id": self.user_id, "fund_id": self.fund_id}
    
#--Get all Users Funds--#
@app.route("/users_funds")
def get_all():
    usersFundsList = UsersFunds.query.all()
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
@app.route("/users_funds/<int:user_id>")
def find_by_user_id(user_id):
    usersFundsList = UsersFunds.query.filter_by(user_id=user_id)
    if usersFundsList:
        usersFundsList = [users_funds.json() for users_funds in usersFundsList]
        return jsonify(
            {
                "code": 200,
                "data": usersFundsList
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "User fund not found."
        }
    ), 404

##-- add a new user fund --##
@app.route("/users_funds", methods=['POST'])
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