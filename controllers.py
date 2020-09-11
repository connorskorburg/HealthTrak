from flask import render_template, redirect, request, flash, session
from config import db 
from models import *
from datetime import datetime, timezone
from better_profanity import profanity
import requests
from secret import *

# render home page
def index():
    return render_template('home.html')
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

def meals():
    if not 'user_id' in session.keys():
        return redirect('/')
    else:
        user = User.query.get(session['user_id'])
        
        all_meals = Meal.query.filter_by(user_id=session['user_id']).all()

        meals = [{
            "id": None,
            "name": "Breakfast",
            "fat": 0,
            "protein": 0,
            "carbs": 0,
            "calories": 0
        },{
            "id": None,
            "name": "Lunch",
            "fat": 0,
            "protein": 0,
            "carbs": 0,
            "calories": 0
        },{
            "id": None,
            "name": "Dinner",
            "fat": 0,
            "protein": 0,
            "carbs": 0,
            "calories": 0
        },{
            "id": None,
            "name": "Snack",
            "fat": 0,
            "protein": 0,
            "carbs": 0,
            "calories": 0
        }]

        for m in all_meals:
            if m.created_at.astimezone().strftime('%Y-%m-%d') == local_time.strftime('%Y-%m-%d'):
                for x in meals:
                    if m.name == x["name"]:
                        x["id"] = m.id
                        x["fat"] = m.total_fat
                        x["protein"] = m.total_protein
                        x["carbs"] = m.total_carbs
                        x["calories"] = m.total_calories

        return render_template('meals.html', user=user, meals=meals, local_time=local_time)
# add food item to meal
def newFood():
    valid_food = Food.validate_food(request.form)
    if not valid_food or request.form['meal_name'] == '':
        return redirect('/meals')
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
            food = Food.create_food(request.form, new_meal.id)
            # ADD FOOD TO MEAL
            new_meal.food_items.append(food)
            db.session.commit()
            # find total calories, fat, carbs, protein of meal and log
            addFoodLog(food, new_meal, log_exists, request.form) 
        elif existing_meal != False:
            # create food
            food = Food.create_food(request.form, existing_meal.id)
            # add food to meal
            existing_meal.food_items.append(food)
            db.session.commit()
            # find total calories of meal
            addFoodLog(food, existing_meal, log_exists, request.form)
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

# food categories and exercise categories
def search():
    if not 'user_id' in session.keys():
        return redirect('/')
    else:
        if request.form['search'] == '':
            return redirect('/')
        else:
            session['search'] = request.form['search']
            return redirect('/searchResults')

# show search results
def searchResults():
    if not 'user_id' in session.keys():
        return redirect('/')
    else:
        search = session['search']
        params = {'api_key': key}
        data = {'generalSearchInput': search}
        response = requests.post(
            r'https://api.nal.usda.gov/fdc/v1/search',
            params=params,
            json=data
        )
        result = response.json()
        results = []
        for i in range(0,5):
            for y in result['foods'][i]['foodNutrients']:
                if y['nutrientName'] == 'Total lipid (fat)':
                    fat = y['value']
                if y['nutrientName'] == 'Carbohydrate, by difference':
                    carbs = y['value']
                if y['nutrientName'] == 'Protein':
                    protein = y['value']
            results.append({
                "description":  result['foods'][i]['description'],
                "protein":  protein,
                "fat":  fat,
                "carbs":  carbs,
            })
        return render_template('results.html', search=search, results=results)


def foodQuery():
    if not 'user_id' in session.keys():
        return redirect('/')
    else:
        user = User.query.get(session['user_id'])
        description = request.form['description'] 
        fat = float(request.form['fat']) 
        carbs = float(request.form['carbs']) 
        protein = float(request.form['protein'])
        calories = float((fat * 9) + (carbs * 4) + (protein * 4)) 
        food = {
            "description": description,
            "fat": fat,
            "carbs": carbs,
            "protein": protein,
            "calories": calories
        }
        return render_template("newFood.html", food=food, user=user)
        


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
            if float(request.form['calories']) != float(food.calories) or float(request.form['fat']) != float(food.fat) or float(request.form['carbs']) != float(food.carbs) or float(request.form['protein']) != float(food.protein):
                # update daily log calories
                updateFoodLog(food, meal, log_exists, request.form)
            # update food item
            food.name = request.form['food_name']
            food.carbs = request.form['carbs']
            food.fat = request.form['fat']
            food.protein = request.form['protein']
            food.calories = request.form['calories']
            food.quantity = request.form['quantity']
            food.public = request.form['public']
            food.category = request.form['category']
            db.session.commit()
            return redirect('/dashboard')
        else:
            return redirect(f'/fooditem/edit/{food.id}')
# delete food item
def deleteFood(food_id):
    if not 'user_id' in session.keys():
        return redirect('/')
    else:
        log_exists = DailyLog.log_exists()
        if log_exists:
            food = Food.query.get(int(food_id))
            meal = Meal.query.get(food.meal_id)
            # remove calories from meal
            deleteFoodLog(food, meal, log_exists)
            return redirect('/dashboard')
        else:
            return redirect('/dashboard')


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
# delete workout
def deleteWorkout(workout_id):
    if not 'user_id' in session.keys():
        return redirect('/')
    else:
        log_exists = DailyLog.log_exists()
        if log_exists:
            workout = Workout.query.get(int(workout_id))
            # remove daily calories burned from workout
            log_exists.calories_burned = float(log_exists.calories_burned) - float(workout.calories_burned)
            db.session.commit()
            # remove daily duration from workout
            log_exists.minutes_worked_out = float(log_exists.minutes_worked_out) - float(workout.duration)
            db.session.commit()
            # delete workout
            db.session.delete(workout)
            db.session.commit()
            return redirect('/fitness')
        else:
            return redirect('/dashboard')


# create exercise and add it to workout
def newExercise():
    if not 'user_id' in session.keys():
        return redirect('/')
    else:
        valid_ex = Exercise.valid_ex(request.form)
        log_exists = DailyLog.log_exists()
        if valid_ex and log_exists:
            duration = calcMinutes(request.form['hour'], request.form['minutes'])
            exercise = Exercise.create_exercise(request.form)
            workout = Workout.query.get(request.form['workout_id'])
            # update workout duration
            workout.duration = float(workout.duration) + float(duration)
            workout.exercises.append(exercise)
            db.session.commit()
            # add workout calories burned
            workout.calories_burned = float(workout.calories_burned) + float(request.form['calories_burned'])
            db.session.commit()
            # add duration to daily log
            log_exists.minutes_worked_out = float(log_exists.minutes_worked_out) + float(duration)
            db.session.commit()
            # add calories burned
            log_exists.calories_burned = float(log_exists.calories_burned) + float(request.form['calories_burned'])
            db.session.commit()
            return redirect('/fitness')
        else:
            return redirect('/fitness')

# render edit exercise page
def editExercise(exercise_id):
    if not 'user_id' in session.keys():
        return redirect('/')
    else:
        user = User.query.get(session['user_id'])
        exercise = Exercise.query.get(int(exercise_id))
        minutes = float(exercise.duration) % 60
        print(minutes)
        hours = (float(exercise.duration) - minutes) / float(60)
        print(hours)
        return render_template('editExercise.html', user=user, exercise=exercise, minutes=minutes, hours=hours)
# post method to update exercise
def updateExercise():
    if not 'user_id' in session.keys():
        return redirect('/')
    exercise = Exercise.query.get(int(request.form['exercise_id']))
    workout = Workout.query.get(exercise.workout_id)
    log_exists = DailyLog.log_exists()
    if log_exists == False:
        return redirect('/dashboard')
    else:
        valid_ex = Exercise.valid_ex_update(request.form)
        if valid_ex and log_exists:
            duration = calcMinutes(float(request.form['hours']), float(request.form['minutes']))
            if float(exercise.calories_burned) != float(request.form['calories_burned']):
                # update daily cals burned
                log_exists.calories_burned = float(log_exists.calories_burned) - float(exercise.calories_burned) + float(request.form['calories_burned'])
                db.session.commit()
                # update worlout cals burned
                workout.calories_burned = float(workout.calories_burned) - float(exercise.calories_burned) + float(request.form['calories_burned'])
                db.session.commit()
            # update total minutes working out
            log_exists.minutes_worked_out = float(log_exists.minutes_worked_out) - float(exercise.duration) + float(duration)
            db.session.commit()
            # update duration for workout
            workout.duration = float(workout.duration) - float(exercise.duration) + float(duration)
            db.session.commit()
            # update exercise
            exercise.name = request.form['exercise_name']
            exercise.duration = duration
            exercise.calories_burned = float(request.form['calories_burned'])
            if request.form['category'] == 'running' or request.form['category'] == 'walking' or request.form['category'] == 'cycling':
                exercise.pace = float(duration) / float(exercise.miles)
                db.session.commit()
            db.session.commit()
            return redirect('/dashboard')
        else:
            return redirect(f'/exercise/edit/{exercise.id}')
# delete exercise
def deleteExercise(exercise_id):
    if not 'user_id' in session.keys():
        return redirect('/')
    else:
        exercise = Exercise.query.get(int(exercise_id))
        workout = Workout.query.get(exercise.workout_id)
        log_exists = DailyLog.log_exists()
        if exercise and log_exists and workout:
            # update daily log cals burned
            log_exists.calories_burned = float(log_exists.calories_burned) - float(exercise.calories_burned)
            db.session.commit()
            # update daily log minutes worked out
            log_exists.minutes_worked_out = float(log_exists.minutes_worked_out) - float(exercise.duration)
            db.session.commit()
            # update workout cals burned
            workout.calories_burned = float(workout.calories_burned) - float(exercise.calories_burned)
            db.session.commit()
            # update workout duration
            workout.duration = float(workout.duration) - float(exercise.duration)
            db.session.commit()
            # delete exercise
            db.session.delete(exercise)
            db.session.commit()
            return redirect('/dashboard')
        else:
            return redirect('/')
# show daily log
def showLog():
    if not 'user_id' in session.keys():
        return redirect('/')
    else:
        user = User.query.get(session['user_id'])
        logs = DailyLog.query.filter_by(user_id=user.id).all()
        parsedLogs = []
        for log in logs:
            parsedLogs.append(
                {
                    "id": log.id,
                    "calories_consumed": log.calories_consumed,
                    "calories_burned": log.calories_burned,
                    "minutes_worked_out": log.minutes_worked_out,
                    "total_fat": log.total_fat,
                    "total_carbs": log.total_carbs,
                    "total_protein": log.total_protein,
                    "created_at": log.created_at.astimezone().strftime("%m-%d-%Y"),
                    "updated_at": log.updated_at.astimezone().strftime("%m-%d-%Y")
                }
            )
        print(parsedLogs)
        return render_template("calendar.html", user=user, logs=parsedLogs)

# show all status
def stats():
    if not 'user_id' in session.keys():
        return redirect('/')
    else:
        log = DailyLog.log_exists()
        user = User.query.get(session['user_id'])
        return render_template("stats.html", user=user, log=log)
        


# render updated dashboard for styling
def newDash():
    if not 'user_id' in session.keys():
        return redirect('/')
    else:
        log_exists = DailyLog.log_exists()
        if log_exists == False:
            new_log = DailyLog(user_id=session['user_id'])
            db.session.add(new_log)
            db.session.commit()
        user = User.query.get(session['user_id'])
        
        all_meals = Meal.query.filter_by(user_id=session['user_id']).all()

        meals = [{
            "name": "Breakfast",
            "fat": 0,
            "protein": 0,
            "carbs": 0,
            "calories": 0
        },{
            "name": "Lunch",
            "fat": 0,
            "protein": 0,
            "carbs": 0,
            "calories": 0
        },{
            "name": "Dinner",
            "fat": 0,
            "protein": 0,
            "carbs": 0,
            "calories": 0
        },{
            "name": "Snack",
            "fat": 0,
            "protein": 0,
            "carbs": 0,
            "calories": 0
        }]

        for m in all_meals:
            if m.created_at.astimezone().strftime('%Y-%m-%d') == local_time.strftime('%Y-%m-%d'):
                for x in meals:
                    if m.name == x["name"]:
                        x["fat"] = m.total_fat
                        x["protein"] = m.total_protein
                        x["carbs"] = m.total_carbs
                        x["calories"] = m.total_calories
        
        workouts = Workout.query.filter_by(user_id=session['user_id']).all()
        workout_count = 0
        for w in workouts:
            if w.created_at.astimezone().strftime('%Y-%m-%d') == local_time.strftime('%Y-%m-%d'):
                workout_count = workout_count + 1


        return render_template('newDash.html', user=user, local_time=local_time, log=log_exists, meals=meals, workout_count=workout_count)