import bcrypt
from flask import Flask, request, session, redirect, url_for, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import sys


from sqlalchemy import null
sys.path.append("../")

app = Flask(__name__)
cors =CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/stonks' # remove :root for non-mac
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'insertsecretkeypassword'

db = SQLAlchemy(app)
bcrypt=Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    __tablename__ = 'users'

    account_id = db.Column(db.Integer, primary_key=True) #fintech account
    username = db.Column(db.String(16),nullable=False) #fintech account username
    password = db.Column(db.String(20), nullable=False) #fintech account password
    name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.String, nullable=False) #t-bank RIB user id
    user_pin = db.Column(db.Integer, nullable=False) #t-bank RIB user pin
    settlement_account = db.Column(db.Integer,nullable=False) #t-bank deposit account

    def __init__(self, account_id, username, password, name, user_id, user_pin, settlement_account):
        self.account_id = account_id
        self.username = username
        self.password = password
        self.name = name
        self.user_id = user_id
        self.user_pin = user_pin
        self.settlement_account = settlement_account

    def json(self):
        return {"account_id": self.account_id, "username": self.username, "password": self.password, "name": self.name , "user_id": self.user_id , "user_pin": self.user_pin ,  "settlement_account": self.settlement_account}

# registration form set up (& validation) username, password & submit button.
class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Register')

    # check if username already exist
    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError("The username '" + existing_user_username + "' already exists. Please choose a different one.")

# login form set up (& validation) username, password & submit button.
class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=16)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')

# landing page
@app.route('/')
def index():
    return render_template('index.html')

# login - check user exists and check if hashed password match
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                flash('Logged in successfully.')
                return redirect(url_for('index'))
    return render_template('login.html', form=form)

# register - validate form, hash password and add+commit new user to db.
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# logout - route back to login
@app.route('/logout', methods=['GET' , 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010, debug=True)