from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_cors import CORS, cross_origin
from flask_wtf.csrf import CSRFProtect
import ENV

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ENV.SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = ENV.SECRET_KEY
app.config['WTF_CSRF_SECRET_KEY'] = ENV.WTF_CSRF_SECRET_KEY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = ENV.SQLALCHEMY_TRACK_MODIFICATIONS

''' 
	CSRF protection requires a secret key to securely sign the token. 
	By default this will use the Flask app's SECRET_KEY. 
	If you'd like to use a separate token you can set WTF_CSRF_SECRET_KEY.
		https://flask-wtf.readthedocs.io/en/stable/csrf.html
'''

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in first'
login_manager.login_message_category = 'info'
login_manager.session_protection = 'strong'

''' 
	Any view using FlaskForm to process the request 
    is already getting CSRF protection. If you have
    views that don't use FlaskForm or make AJAX requests, 
    use the provided CSRF extension to protect those requests as well.

'''
# csrf = CSRFProtect(app)  # same as below
# CORS(app)


from app import routes

