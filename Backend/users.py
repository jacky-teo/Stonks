from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS  # enable CORS

app = Flask(__name__)
cors =CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/stonks'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)

    def __init__(self, user_id, username, password):
        self.user_id = user_id
        self.username = username
        self.password = password

    def json(self):
        return {"user_id": self.user_id, "username": self.username, "password": self.password}

#--Get all Users--#
@app.route("/users")
def get_all():
    usersList = Users.query.all()
    if len(usersList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "users": [users.json() for users in usersList]
                }
            }
        ),200
    return jsonify(
        {
            "code": 404,
            "message": "There are no users."
        }
    ), 404

#get user by username
@app.route("/users/<string:username>")
def find_by_username(username):
    usersList = Users.query.filter_by(username=username)
    if usersList:
        usersList = [users.json() for users in usersList]
        return jsonify(
            {
                "code": 200,
                "data": usersList
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "message": "User not found."
        }
    ), 404



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)