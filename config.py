from flask import Flask 
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from secret import secret_key, uri

app = Flask(__name__)

app.secret_key = secret_key

app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)
db.create_all()
db.session.commit()

bcrypt = Bcrypt(app)

