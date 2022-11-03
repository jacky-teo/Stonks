from sqlalchemy.exc import SQLAlchemyError
from flask import Flask, request, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS  # enable CORS
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from itsdangerous import json
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
cors =CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/stonks'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/stonks'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'insertsecretkeypassword'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    user_acc_id = db.Column(db.String(50), nullable=False)
    user_pin = db.Column(db.Integer, nullable=False)
    settlement_acc = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, username, password, user_acc_id, user_pin, settlement_acc):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.user_acc_id = user_acc_id
        self.user_pin = user_pin
        self.settlement_acc = settlement_acc

    def json(self):
        return {"user_id": self.user_id, "username": self.username, "password": self.password, "user_acc_id": self.user_acc_id, "user_pin": self.user_pin, "settlement_acc": self.settlement_acc}

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.user_id)

@app.route('/user_info/user/<int:user_id>', methods=['GET', 'POST'])
def get_user_id_user_pin(user_id):
    user = Users.query.filter_by(user_id=user_id).first()
    if user:
        print(user.json())

        return jsonify({
            "result": 200,
            "data": {
                'user_acc_id': user.user_acc_id,
                'user_pin': user.user_pin,
                'settlement_acc': user.settlement_acc
            }
        }), 200
    else:
        return jsonify({
            "result": 401,
            "message": "No user info"
        }), 401

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

# login - check user exists and check if hashed password match
@app.route('/login', methods=['GET', 'POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    user = Users.query.filter_by(username=username).first()

    # !!!! uncomment this when you want to test accounts that were hardcoded into the db !!!!
    # if not user or not user.password == password:
    #     return jsonify({
    #         "result": 401,
    #         "status": "failed",
    #         "message": "Failed getting user"
    #     }), 401

    # "check_password_hash(user.password, password)" used for all the newly created accounts with hashed password
    if not user or not check_password_hash(user.password, password):
        return jsonify({
            "result": 401,
            "status": "failed",
            "message": "Failed getting user"
        }), 401

    else:
        # flask_login - session created
        login_user(user, remember=True)
        return jsonify({
            "result": 200,
            "status": "success",
            "message": "Login successful",
            
            "data": {
                "id": user.user_id,
                "username": user.username
            }
        }), 200

# register - validate form, hash password and add+commit new user to db
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user_id = None
    username = data.get("username")
    password = generate_password_hash(data.get("password"), method='sha256')
    user_acc_id = data.get('user_acc_id')
    user_pin = int(data.get('user_pin'))
    settlement_acc = int(data.get('settlement_acc'))
    newUser = Users(user_id=user_id, username=username, password=password, user_acc_id=user_acc_id, user_pin=user_pin,settlement_acc=settlement_acc)

    try:
        # newUser = Users(user_id, username=username, password=password, user_acc_id=user_acc_id, user_pin=user_pin,settlement_acc=settlement_acc)
        db.session.add(newUser)
        db.session.commit()

    except SQLAlchemyError as e:
        error = str(e.orig)
        return jsonify({
            "result": 404,
            "status": "error",
            "message": "Could not add user",
            "errmsg": error
        }), 404

    # flask_login - session created
    login_user(newUser, remember=True)
    return jsonify({
        "result": 201,
        "status": "success",
        "message": "User added successfully",
        "data": newUser.json()
    }), 201

# logout - route back to login
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    # flask_login - session cleared
    logout_user()
    return jsonify({
        "result": 200,
        "status": "success",
        "message": "logout successfully"
    }), 200

# get info of logged in user
@app.route('/user_info', methods=['GET', 'POST'])
@login_required
def user_info():
    if current_user.is_authenticated:
        return jsonify({
            "result": 200,
            "data": current_user.json()
        }), 200
    else:
        return jsonify({
            "result": 401,
            "message": "No user info, user not logged in"
        }), 401




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)