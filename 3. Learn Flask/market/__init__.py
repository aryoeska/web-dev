from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__) # set up out application
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:010202@localhost/market'
db = SQLAlchemy(app)

from market import routes

