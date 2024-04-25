from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__) # set up out application
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:010202@localhost/market'
app.config['SECRET_KEY'] = '57a90d75d390273247c7506a'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from market import routes

