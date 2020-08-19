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
        return render_template('dashboard.html', user=user, local_time=local_time)
# register user 
def register():
    valid_user = User.validate_user(request.form)
    print(valid_user)
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
            new_meal.total_calories = float(new_meal.total_calories) + float(food.calories)
            db.session.commit()
        elif existing_meal != False:
            # food = Food.create_food(request.form)
            existing_meal.food_in_meal.append(food)
            existing_meal.total_calories = float(existing_meal.total_calories) + float(food.calories)
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
# render template for adding workout/exercise
def fitness():
    if not 'user_id' in session.keys():
        return redirect('/')
    else:
        user = User.query.get(session['user_id'])
        workouts = Workout.query.filter_by(user_id=session['user_id'])
        daily_workouts = []
        for w in workouts:
            if w.created_at.astimezone().strftime('%Y-%m-%d') == local_time.strftime('%Y-%m-%d'):
                daily_workouts.append(w)
        return render_template('workout.html', user=user, workouts=daily_workouts)
# post method to add new workout
def newWorkout():
    if not 'user_id' in session.keys():
        return redirect('/')
    else:
        if request.form['workout_name'] == '':
            flash("Please Enter a Workout Name", "workout_error")
            return redirect('/fitness')
        else:
            workout = Workout(name=request.form['workout_name'], user_id=session['user_id'])
            db.session.add(workout)
            db.session.commit()
            return redirect('/fitness')
# create exercise and add it to workout
def newExercise():
    if not 'user_id' in session.keys():
        return redirect('/')
    else:
        valid_ex = Exercise.valid_exercise(request.form)
        if valid_ex:
            exercise = Exercise.create_exercise(request.form)
            workout = Workout.query.get(request.form['workout_id'])
            workout.exercise_in_workout.append(exercise)
            db.session.commit()
            return redirect('/fitness')
        else:
            return redirect('/fitness')