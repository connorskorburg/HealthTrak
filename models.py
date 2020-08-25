from sqlalchemy.sql import func 
from config import db, bcrypt
from flask import flash, request, session
import re
from datetime import datetime, timezone
from better_profanity import profanity 

utc = datetime.now(timezone.utc)
local_time = utc.astimezone()

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

def calcMinutes(hour, minutes):
    h = float(hour)
    m = float(minutes)
    return float((h * 60) + m)

def addFoodLog(food, meal, log, user_data):
    # update and save meal
    meal.total_calories = float(meal.total_calories) + float(food.calories)
    meal.total_fat = float(meal.total_fat) + float(user_data['fat'])
    meal.total_carbs = float(meal.total_carbs) + float(user_data['carbs'])
    meal.total_protein = float(meal.total_protein) + float(user_data['protein'])
    db.session.commit()
    # update log and save
    log.calories_consumed = float(log.calories_consumed) + float(food.calories)
    log.total_fat = float(log.total_fat) + float(user_data['fat'])
    log.total_carbs = float(log.total_carbs) + float(user_data['carbs'])
    log.total_protein = float(log.total_protein) + float(user_data['protein'])
    db.session.commit() 

def updateFoodLog(food, meal, log, user_data):
    # update meal and save meal
    meal.total_calories = float(meal.total_calories) - float(food.calories) + float(request.form['calories'])
    meal.total_fat = float(meal.total_fat) - float(food.fat) + float(request.form['fat'])
    meal.total_carbs = float(meal.total_carbs) - float(food.carbs) + float(request.form['carbs'])
    meal.total_protein = float(meal.total_protein) - float(food.protein) + float(request.form['protein'])
    db.session.commit()
    # update log and save log
    log.calories_consumed = float(log.calories_consumed) - float(food.calories) + float(request.form['calories'])
    log.total_fat = float(log.total_fat) - float(food.fat) + float(request.form['fat'])
    log.total_carbs = float(log.total_carbs) - float(food.carbs) + float(request.form['carbs'])
    log.total_protein = float(log.total_protein) - float(food.protein) + float(request.form['protein'])
    db.session.commit()

def deleteFoodLog(food, meal, log):
    # remove info from meal and log
    meal.total_calories = float(meal.total_calories) - float(food.calories)
    meal.total_fat = float(meal.total_fat) - float(food.fat)
    meal.total_carbs = float(meal.total_carbs) - float(food.carbs)
    meal.total_protein = float(meal.total_protein) - float(food.protein)
    db.session.commit()
    # remove info from log
    log.calories_consumed = float(log.calories_consumed) - float(food.calories)
    log.total_fat = float(log.total_fat) - float(food.fat)
    log.total_carbs = float(log.total_carbs) - float(food.carbs)
    log.total_protein = float(log.total_protein) - float(food.protein)
    db.session.commit()
    # delete food
    db.session.delete(food)
    db.session.commit()

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
    workout_history = db.relationship('Workout', back_populates='user', cascade='all, delete, delete-orphan')
    meals = db.relationship('Meal', back_populates='user', cascade='all, delete, delete-orphan')
    log_history = db.relationship('DailyLog', back_populates='user', cascade='all, delete, delete-orphan')
    @classmethod 
    def validate_user(cls, user_data):
        is_valid = True 
        if len(user_data['first_name']) < 1:
            is_valid = False 
            flash("Please Enter a Valid First Name", "reg_error")
        if profanity.contains_profanity(user_data['first_name']) == True:
            is_valid = False
            flash("Please Enter an Appropriate First Name", "reg_error");
        if len(user_data['last_name']) < 1:
            is_valid = False 
            flash("Please Enter a Valid Last Name", "reg_error")
        if profanity.contains_profanity(user_data['last_name']) == True:
            is_valid = False
            flash("Please Enter an Appropriate Last Name", "reg_error");
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

class DailyLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    calories_consumed = db.Column(db.Float, default=0)
    calories_burned = db.Column(db.Float, default=0)
    minutes_worked_out = db.Column(db.Float, default=0)
    total_fat = db.Column(db.Float, default=0)
    total_carbs = db.Column(db.Float, default=0)
    total_protein = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='cascade'), nullable=False)
    user = db.relationship('User', foreign_keys=[user_id])
    @classmethod
    def log_exists(cls):
        all_logs = DailyLog.query.filter_by(user_id=session['user_id']).all()
        log = ''
        for l in all_logs:
            if l.created_at.astimezone().strftime('%Y-%m-%d') == local_time.strftime('%Y-%m-%d'):
                log = l
        if log != '':
            return log
        elif log == '':
            return False  

class Sleep(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='cascade'), nullable=False)
    user = db.relationship('User', foreign_keys=[user_id])

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    duration = db.Column(db.Float, default=0)
    calories_burned = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='cascade'), nullable=False)
    user = db.relationship('User', foreign_keys=[user_id])
    exercises = db.relationship('Exercise', back_populates='workout', cascade='all, delete, delete-orphan')

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    duration = db.Column(db.Float)
    calories_burned = db.Column(db.Integer)
    category = db.Column(db.String(45), nullable=False)
    pace = db.Column(db.Float(), nullable=True)
    miles = db.Column(db.Float(), nullable=True)
    sets = db.Column(db.Float(), nullable=True)
    reps = db.Column(db.Float(), nullable=True)
    description = db.Column(db.Text(), nullable=True)
    public = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id', ondelete='cascade'), nullable=False)
    workout = db.relationship('Workout', foreign_keys=[workout_id])
    # class methods
    @classmethod
    def valid_exercise(cls, user_data):
        is_valid = True
        if user_data['workout_id'] == '':
            is_valid = False
        if len(user_data['exercise_name']) < 2 or user_data['exercise_name'] == '':
            is_valid = False
            flash("Please Enter an Exercise Name", "ex_error")
        if profanity.contains_profanity(user_data['exercise_name']) == True:
            is_valid = False
            flash("Please Enter an Appropriate Exercise Name", "ex_error");
        if user_data['hour'] == '':
            is_valid = False
            flash("Please Enter Amount of Hours", "ex_error")
        if user_data['minutes'] == '':
            is_valid = False
            flash("Please Enter Amount of Minutes", "ex_error")
        if user_data['calories_burned'] == '':
            is_valid = False
            flash("Please Enter Est. Calories Burned", "ex_error")
        return is_valid
    @classmethod
    def create_exercise(cls, user_data):
        duration = calcMinutes(user_data['hour'], user_data['minutes'])
        exercise = Exercise(name=user_data['exercise_name'], duration=duration, calories_burned=user_data['calories_burned'], workout_id=user_data['workout_id'])
        db.session.add(exercise)
        db.session.commit()
        return exercise 
    @classmethod
    def valid_ex_update(cls, user_data):
        is_valid = True
        if user_data['calories_burned'] == '':
            is_valid = False
            flash("Please Enter Est. Calories Burned", "ex2_error")
        if len(user_data['exercise_name']) < 2 or user_data['exercise_name'] == '':
            is_valid = False
            flash("Please Enter an Exercise Name", "ex2_error")
        if profanity.contains_profanity(user_data['exercise_name']) == True:
            is_valid = False
            flash("Please Enter an Appropriate Exercise Name", "ex2_error");
        if user_data['duration'] == '' or float(user_data['duration']) < 1:
            is_valid = False
            flash("Please Enter Duration", "ex2_error")
        return is_valid 
    @classmethod
    def valid_ex(cls, user_data):
        is_valid = True
        if len(user_data['exercise_name']) < 2 or user_data['exercise_name'] == '':
            is_valid = False
            flash("Please Enter an Exercise Name", "ex_error")
        if profanity.contains_profanity(user_data['exercise_name']) == True:
            is_valid = False
            flash("Please Enter an Appropriate Exercise Name", "ex_error");
        if user_data['hour'] == '':
            is_valid = False
            flash("Please Enter Amount of Hours", "ex_error")
        if user_data['minutes'] == '':
            is_valid = False
            flash("Please Enter Amount of Minutes", "ex_error")
        if user_data['calories_burned'] == '':
            is_valid = False
            flash("Please Enter Est. Calories Burned", "ex_error")
        if user_data['category'] == 'running' or user_data['category'] == 'walking' or user_data['category'] == 'cycling':
            if user_data['pace_min'] == '':
                is_valid = False
                flash("Please Enter Minutes for Pace", "ex_error")
            if user_data['pace_sec'] == '':
                is_valid = False
                flash("Please Enter Seconds for Pace", "ex_error")
            if user_data['miles'] == '' or user_data['miles'] == 0:
                is_valid = False
                flash("Please Enter Amount of Miles", "ex_error")
        if user_data['category'] == 'weight_lifting':
            if user_data['reps'] == '':
                is_valid = False
                flash("Please Enter Amount of Repetitions", "ex_error")
            if user_data['sets'] == '':
                is_valid = False
                flash("Please Enter Amount of Sets", "ex_error")
        if user_data['category'] == 'other':
            if user_data['desc'] == '' or profanity.contains_profanity(user_data['desc']) == True:
                is_valid = False
                flash("Please Enter Valid Description", "ex_error")
        return is_valid


class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    total_calories = db.Column(db.Float, default=0)
    total_fat = db.Column(db.Float, default=0)
    total_carbs = db.Column(db.Float, default=0)
    total_protein = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='cascade'), nullable=False)
    user = db.relationship('User', foreign_keys=[user_id])
    food_items = db.relationship('Food', back_populates='meal', cascade='all, delete, delete-orphan')
    @classmethod
    def meal_exists(cls, user_data):
        all_meals = Meal.query.filter_by(user_id=session['user_id']).filter_by(name=user_data['meal_name'])
        print(all_meals)
        meal = ''
        for m in all_meals:
            if m.created_at.astimezone().strftime('%Y-%m-%d') == local_time.strftime('%Y-%m-%d'):
                meal = m
                print(meal)
        if meal != '':
            return meal
        elif meal == '':
            return False                

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    calories = db.Column(db.Float)
    name = db.Column(db.String(100), nullable=False)
    carbs = db.Column(db.Float, nullable=False)
    fat = db.Column(db.Float, nullable=False)
    protein = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(45))
    public = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    meal_id = db.Column(db.Integer, db.ForeignKey('meal.id', ondelete='cascade'), nullable=False)
    meal = db.relationship('Meal', foreign_keys=[meal_id])
    # class methods
    @classmethod
    def validate_food(cls, user_data):
        is_valid = True
        if len(user_data['food_name']) < 1:
            is_valid = False
            flash("Please Enter A Food Name", "food_error")
        if profanity.contains_profanity(user_data['food_name']) == True:
            is_valid = False
            flash("Please Enter an Appropriate Food Name", "food_error");
        if user_data['calories'] == '':
            is_valid = False 
            flash("Please Enter Calories for Food Item", "food_error")
        if user_data['category'] == '':
            is_valid = False
            flash("Please Select a Food Category", "reg_error")
        if user_data['carbs'] == '' or float(user_data['carbs']) <=0:
            is_valid = False
            flash("Please Enter Carbs for Food Item", "food_error")
        if user_data['fat'] == '' or float(user_data['fat']) <=0:
            is_valid = False
            flash("Please Enter Fat for Food Item", "food_error")
        if user_data['protein'] == '' or float(user_data['protein']) <=0:
            is_valid = False
            flash("Please Enter Protein for Food Item", "food_error")
        if user_data['quantity'] == '' or float(user_data['quantity']) <=0:
            is_valid = False
            flash("Please Enter Quantity of Food Items", "food_error")
        if user_data['public'] == '':
            is_valid = False
            flash("Please Select a Public or Private option", "food_error")
        return is_valid
    @classmethod
    def create_food(cls, user_data, meal_id):
        food = Food(calories=user_data['calories'], name=user_data['food_name'], carbs=user_data['carbs'], fat=user_data['fat'], protein=user_data['protein'], quantity=user_data['quantity'], public=user_data['public'] ,category=user_data['category'], meal_id=int(meal_id))
        db.session.add(food)
        db.session.commit()
        return food


db.create_all()
db.session.commit()