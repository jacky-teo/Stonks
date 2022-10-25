from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS  # enable CORS



app = Flask(__name__)
cors =CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/stonks'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class FundsUsersStocks(db.Model):
    __tablename__ = 'funds_users_stocks'

    fund_id = db.Column(db.Integer, primary_key=True)
    user_stock_id = db.Column(db.Integer, primary_key=True)
   
    def __init__(self, fund_id, user_stock_id):
        self.fund_id = fund_id
        self.user_stock_id = user_stock_id
    
    def json(self):
        return {"fund_id": self.fund_id, "user_stock_id": self.user_stock_id}


#--Get all Funds settlement id--#
@app.route("/funds_users_stocks")
def get_all():
    fundsUsersStocks = FundsUsersStocks.query.all()
    if len(fundsUsersStocks):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "fundsSettlement": [fundsuserStock.json() for fundsuserStock in fundsUsersStocks]
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
@app.route("/funds_users_stocks/<int:fund_id>")
def find_by_fund_id(fund_id):
    fundSettlement = FundsUsersStocks.query.filter_by(fund_id=fund_id)
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
@app.route("/funds_users_stocks/add", methods=['POST'])
def create_fund_settlement():
    data = request.get_json()
    fundSettlement = FundsUsersStocks(**data)
    try:
        db.session.add(fundSettlement)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "fund_id": fundSettlement.fund_id,
                    "user_stock_id": fundSettlement.user_stock_id
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)