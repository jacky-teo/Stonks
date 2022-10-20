from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS  # enable CORS

app = Flask(__name__)
cors =CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/stonks'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Marketplace(db.Model):
    __tablename__ = 'marketplace'

    marketplace_id = db.Column(db.Integer, primary_key=True)
    marketplace_name=db.Column(db.String(50), nullable=False)
    
    def __init__(self, marketplace_id, marketplace_name):
        self.marketplace_id = marketplace_id
        self.marketplace_name = marketplace_name


    
    def json(self):
        return {"marketplace_id": self.marketplace_id, "marketplace_name": self.marketplace_name}

#--Get all Marketplace--#
@app.route("/marketplace")
def get_all():
    marketplaceList = Marketplace.query.all()
    if len(marketplaceList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "marketplace": [marketplace.json() for marketplace in marketplaceList]
                }
            }
        ),200
    return jsonify(
        {
            "code": 404,
            "message": "There are no marketplace."
        }
    ), 404

# --Get Marketplace by marketplace_id--#
@app.route("/marketplace/<int:marketplace_id>")
def find_by_marketplace_id(marketplace_id):
    marketplace = Marketplace.query.filter_by(marketplace_id=marketplace_id).first()
    if marketplace:
        return jsonify(
            {
                "code": 200,
                "data": marketplace.json()
            }
        ),200
    return jsonify(
        {
            "code": 404,
            "data": {
                "marketplace_id": marketplace_id
            },
            "message": "Marketplace not found."
        }
    ), 404