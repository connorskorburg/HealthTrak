from flask import render_template, redirect, request, flash, session
from config import db 
from models import *
from datetime import datetime, timezone

# render home page
def home():
    return render_template('index.html')
# render dashboard
def dashboard():
    if not 'user_id' in session.keys():
        return redirect('/')
    else:
        user = User.query.get(session['user_id'])
        return render_template('dashboard.html', user=user)
# register user 
def register():
    valid_user = User.validate_user(request.form)
    if not valid_user:
        return redirect('/')
    else:
        user = User.create_user(request.form)
        session['user_id'] = user.id
        return redirect('/dashboard')
# login user
def login():
    user = User.validate_login(request.form)
    session['user_id'] = user.id
    return redirect('/dashboard')
# logout user
def logout():
    session.clear()
    return redirect('/')
# fitness page 
def mealtrack():
    if not 'user_id' in session.keys():
        return redirect('/')
    else:
        user = User.query.get(session['user_id'])
        return render_template('mealtrack.html', user=user)
# add food item to meal
def newFood():
    user = User.query.get(session['user_id'])
    # print(meal.created_at)
    print("CREATED AT:", user.created_at)
    utc = datetime.now(timezone.utc)
    print("UTC:", utc)
    print("LOCAL TZ:", utc.astimezone())
    local = utc.astimezone()
    print("LOCAL TZ DAY OF MONTH:", local.strftime("%d"))
    print("LOCAL TZ TIME:", local.strftime("%H:%M"))
    created = user.created_at
    print("UTC DAY OF MONTH:", utc.strftime("%d"))
    print("CREATED AT DAY OF MONTH:", created.strftime("%d"))
    print("CREATED AT TIME:", created.strftime("%H:%M"))

    print("CREATED AT LOCAL TZ:", created.astimezone())
    print(created.astimezone().strftime("%Z"))
    print("CREATED AT LOCAL TZ DIF:", created.astimezone().strftime("%z"))
    # last_meal = Meal.query.filter_by(user_id = session['user_id']).all()
    # print(last_meal) 
    # print(len(last_meal))
    valid_food = Food.validate_food(request.form)
    if not valid_food:
        return redirect('/mealtrack')
    else:
        if request.form['meal_name'] == '':
            return redirect('/')
        else:
            # if utc.strftime("%d") == 
            return redirect('/mealtrack')
            