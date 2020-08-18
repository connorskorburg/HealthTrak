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
    valid_food = Food.validate_food(request.form)
    if not valid_food or request.form['meal_name'] == '':
        return redirect('/mealtrack')
    else:
        existing_meal = Meal.meal_exists(request.form)
        food = Food.create_food(request.form)
        if existing_meal == False:
            new_meal = Meal(name=request.form['meal_name'], user_id=session['user_id'])
            db.session.add(new_meal)
            db.session.commit()
            new_meal.food_in_meal.append(food)
            db.session.commit()
        elif existing_meal != False:
            # food = Food.create_food(request.form)
            existing_meal.food_in_meal.append(food)
            db.session.commit()
        return redirect('/mealtrack')
# render edit food page
def editFood(food_id):
    if not 'user_id' in session.keys():
        return redirect('/')
    else:
        user = User.query.get(session['user_id'])
        food = Food.query.get(food_id)
        return render_template('editfood.html', user=user, food=food)
# method to update food 
def updateFood():
    food = Food.query.get(request.form['food_id'])
    if not 'user_id' in session.keys():
        return redirect('/')
    else:
        valid_food = Food.validate_food(request.form)
        if valid_food:
            food.name = request.form['food_name']
            food.carbs = request.form['carbs']
            food.fat = request.form['fat']
            food.protein = request.form['protein']
            food.calories = request.form['calories']
            db.session.commit()
            return redirect('/dashboard')
        else:
            return redirect(f'/fooditem/edit/{food.id}')