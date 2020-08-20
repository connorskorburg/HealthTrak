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
        log_exists = DailyLog.log_exists()
        if log_exists == False:
            new_log = DailyLog(user_id=session['user_id'])
            db.session.add(new_log)
            db.session.commit()
        user = User.query.get(session['user_id'])
        return render_template('dashboard.html', user=user, local_time=local_time, log_exists=log_exists)
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
        log_exists = DailyLog.log_exists()
        if log_exists == False:
            return redirect('/dashboard')
        existing_meal = Meal.meal_exists(request.form)
        # food = Food.create_food(request.form)
        if existing_meal == False:
            # CREATE AND SAVE NEW MEAL
            new_meal = Meal(name=request.form['meal_name'], user_id=session['user_id'])
            db.session.add(new_meal)
            db.session.commit()
            # create food
            food = Food(calories=request.form['calories'], name=request.form['food_name'], carbs=request.form['carbs'], fat=request.form['fat'], protein=request.form['protein'], quantity=request.form['quantity'],public=int(request.form['public']), meal_id=new_meal.id)
            db.session.add(food)
            db.session.commit()
            # ADD FOOD TO MEAL
            new_meal.food_items.append(food)
            db.session.commit()
            # find total calories of meal
            total_cals = (float(new_meal.total_calories) + float(food.calories))
            new_meal.total_calories = total_cals
            db.session.commit()
            # add meal calories to daily log
            log_exists.calories_consumed = float(log_exists.calories_consumed) + total_cals
            db.session.commit() 
        elif existing_meal != False:
            # create food
            food = Food(calories=request.form['calories'], name=request.form['food_name'], carbs=request.form['carbs'], fat=request.form['fat'], protein=request.form['protein'], quantity=request.form['quantity'], public=int(request.form['public']), meal_id=existing_meal.id)
            db.session.add(food)
            db.session.commit()
            # add food to meal
            existing_meal.food_items.append(food)
            db.session.commit()
            # find total calories of meal
            total_cals =  (float(existing_meal.total_calories) + float(food.calories))
            existing_meal.total_calories = total_cals
            db.session.commit()
            # add meal calories to daily log
            log_exists.calories_consumed = float(log_exists.calories_consumed) + float(food.calories)
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
    meal = Meal.query.get(food.meal_id)
    if not 'user_id' in session.keys():
        return redirect('/')
    else:
        valid_food = Food.validate_food(request.form)
        log_exists = DailyLog.log_exists()
        if log_exists == False:
            return redirect('/dashboard')
        if valid_food and log_exists:
            if float(request.form['calories']) != float(food.calories):
                # update daily log calories
                log_exists.calories_consumed = float(log_exists.calories_consumed) - float(food.calories) + float(request.form['calories'])
                db.session.commit()
                # update meal calories
                meal.total_calories = float(meal.total_calories) - float(food.calories) + float(request.form['calories'])
                db.session.commit()
            # update food item
            food.name = request.form['food_name']
            food.carbs = request.form['carbs']
            food.fat = request.form['fat']
            food.protein = request.form['protein']
            food.calories = request.form['calories']
            food.quantity = request.form['quantity']
            food.public = request.form['public']
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