from flask import Flask 
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate 


app = Flask(__name__)

app.secret_key = 'health_app_practice'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///health_app_practice.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app0)