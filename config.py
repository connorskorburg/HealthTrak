from flask import Flask 
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy 
# from flask_migrate import Migrate 

app = Flask(__name__)

app.secret_key = 'health_app_practice'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/health_tracker_app_practice'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)

# migrate = Migrate(app, db)

bcrypt = Bcrypt(app)

