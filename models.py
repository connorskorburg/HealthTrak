from sqlalchemy.sql import func 
from config import db, bcrypt
from flask import flash, request, session
import re
from datetime import datetime, timezone

utc = datetime.now(timezone.utc)
local_tz = utc.astimezone()

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def calcCalories(height, weight, sex, age, activity):
    if sex == 1:
        bmr = float((4.536 * weight) + (15.88 * height) - (5 * float(age)) + 5)
        daily_cals = bmr * activity
        return daily_cals
    if sex == 2:
        bmr = float((4.536 * weight) + (15.88 * height) - (5 * float(age)) - 161)
        daily_cals = bmr * activity
        return daily_cals
    else:
        return False

meal_has_food_item = db.Table('meal_has_food_item',
                     db.Column('meal_id', db.Integer, db.ForeignKey('meal.id', ondelete='cascade'), primary_key=True),
                     db.Column('food_id', db.Integer, db.ForeignKey('food.id', ondelete='cascade'), primary_key=True))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    email = db.Column(db.String(100))
    age = db.Column(db.Integer)
    sex = db.Column(db.Integer)
    activity = db.Column(db.Float)
    height = db.Column(db.Float, nullable=True)
    weight = db.Column(db.Float, nullable=True)
    daily_calories = db.Column(db.Float, nullable=True)
    password = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    sleep_history = db.relationship('Sleep', back_populates='user', cascade='all, delete, delete-orphan')
    exercise_history = db.relationship('Exercise', back_populates='user', cascade='all, delete, delete-orphan')
    meals = db.relationship('Meal', back_populates='user', cascade='all, delete, delete-orphan')
    @classmethod 
    def validate_user(cls, user_data):
        is_valid = True 
        if len(user_data['first_name']) < 1:
            is_valid = False 
            flash("Please Enter a Valid First Name", "reg_error")
        if len(user_data['last_name']) < 1:
            is_valid = False 
            flash("Please Enter a Valid Last Name", "reg_error")
        if not EMAIL_REGEX.match(user_data['email']):
            is_valid = False
            flash("Please Enter a Valid Email", "reg_error")
        if request.form['feet'] == '' or request.form['inches'] == '':
            is_valid = False
            flash("Please Enter a Valid Height", "reg_error")
        if len(user_data['weight']) < 1:
            is_valid = False 
            flash("Please Enter a Valid Weight", "reg_error")
        if int(user_data['sex']) != 1 and int(user_data['sex']) != 2:
            is_valid = False
            flash("Please Select Your Sex", "reg_error")
        if float(user_data['activity']) != 1.2 and float(user_data['activity']) != 1.375 and float(user_data['activity']) != 1.55 and float(user_data['activity']) != 1.725 and float(user_data['activity']) != 1.9:
            is_valid = False 
            flash("Please Select Activity Level", "reg_error")
        if len(user_data['password']) < 8:
            is_valid = False 
            flash("Please Enter a Valid Password", "reg_error")
        if user_data['password'] != user_data['confirm_password']:
            is_valid = False 
            flash("Please Enter Matching Passwords", "reg_error")
        return is_valid
    @classmethod
    def create_user(cls, user_data):
        # get user height 
        user_height = float((12 * int(request.form['feet'])) + int(request.form['inches']))
        #get daily calories 
        daily_cals = calcCalories(user_height, float(user_data['weight']), int(user_data['sex']), int(user_data['age']), float(user_data['activity']))
        # hash password w bcrypt
        hashed_password = bcrypt.generate_password_hash(user_data['password'])
        # create user 
        user = cls(first_name=user_data['first_name'], last_name=user_data['last_name'], email=user_data['email'], age=user_data['age'], sex=user_data['sex'], activity=user_data['activity'], height=user_height, weight=float(user_data['weight']), daily_calories=daily_cals, password=hashed_password)
        # save user to db
        db.session.add(user)
        db.session.commit()
        return user
    @classmethod
    def validate_login(cls, user_data):
        if not EMAIL_REGEX.match(user_data['email']):
            user = False
            flash("Please Enter a Valid Email", 'login_error')
        if len(user_data['password']) < 8:
            user = False 
            flash("Please Enter a Valid Password", 'login_error')
        else:
            user = cls.query.filter_by(email=user_data['email']).first()
            if bcrypt.check_password_hash(user.password, user_data['password']):
                return user
            else:
                flash("Password Did Not Match", "login_error")
                return user

class Sleep(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='cascade'), nullable=False)
    user = db.relationship('User', foreign_keys=[user_id])

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    duration = db.Column(db.Float)
    calories_burned = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='cascade'), nullable=False)
    user = db.relationship('User', foreign_keys=[user_id])

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='cascade'), nullable=False)
    user = db.relationship('User', foreign_keys=[user_id])
    food_in_meal = db.relationship('Food', secondary=meal_has_food_item, passive_deletes=True)

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    calories = db.Column(db.Float)
    name = db.Column(db.String(100))
    carbs = db.Column(db.Float, nullable=True)
    fat = db.Column(db.Float, nullable=True)
    protein = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    meal_categories = db.relationship('Food', secondary=meal_has_food_item, passive_deletes=True)
    @classmethod
    def validate_food(cls, user_data):
        is_valid = True
        if len(user_data['food_name']) < 1:
            is_valid = False
            flash("Please Enter A Food Name", "food_error")
        if user_data['calories'] == '':
            is_valid = False 
            flash("Please Enter Calories for Food Item", "food_error")
        return is_valid
    @classmethod
    def create_food(cls, user_data):
        pass

db.create_all()
db.session.commit()