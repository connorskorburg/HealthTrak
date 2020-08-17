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
    # user = User.query.get(session['user_id'])
    # print(meal.created_at)
    # print("CREATED AT:", user.created_at)
    # utc = datetime.now(timezone.utc)
    # print("UTC:", utc)
    # print("LOCAL TZ:", utc.astimezone())
    # local = utc.astimezone()
    # print("LOCAL TZ DAY OF MONTH:", local.strftime("%d"))
    # print("LOCAL TZ TIME:", local.strftime("%H:%M"))
    # created = user.created_at
    # print("UTC DAY OF MONTH:", utc.strftime("%d"))
    # print("CREATED AT DAY OF MONTH:", created.strftime("%d"))
    # print("CREATED AT TIME:", created.strftime("%H:%M"))

    # print("CREATED AT LOCAL TZ:", created.astimezone())
    # print(created.astimezone().strftime("%Z"))
    # print("CREATED AT LOCAL TZ DIF:", created.astimezone().strftime("%z"))
    # if '-' in created.astimezone().strftime("%z"):
    #     print("NEGATIVE")
    #     new_created = created.astimezone().strftime("%z")
    #     print(new_created[0], new_created[1], new_created[2])
    #     new_created_tz = int(new_created[1] + new_created[2])
    #     print(new_created_tz)
    #     print("")

bcrypt = Bcrypt(app)

