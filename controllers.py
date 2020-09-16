from flask import render_template, redirect, request, flash, session
from config import db 
from models import *
from datetime import datetime, timezone
from better_profanity import profanity
import requests
from secret import *
from FoodController import *
from FitnessController import *


def createLog():
    if not 'user_id' in session.keys():
        return redirect('/')
    else:
        log_exists = DailyLog.log_exists()
        if log_exists == False:
            new_log = DailyLog(user_id=session['user_id'])
            db.session.add(new_log)
            db.session.commit()
            session['log_id'] = new_log.id
            return redirect('/dashboard')
        else:
            return redirect('/')



# render home page
def index():
    return render_template('home.html')



def reg():
    return render_template('reg.html')
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
    if user != False:
        session['user_id'] = user.id
        return redirect('/dashboard')
    else:
        return redirect('/')
# logout user
def logout():
    session.clear()
    return redirect('/')


      

# show daily log
def showLog():
    if not 'user_id' in session.keys():
        return redirect('/')
    else:
        log_exists = DailyLog.log_exists()
        if log_exists == False:
            return redirect('/createLog')
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
            return render_template("calendar.html", user=user, logs=parsedLogs)

        


# render updated dashboard for styling
def dashboard():
    if not 'user_id' in session.keys():
        return redirect('/')
    else:
        log_exists = DailyLog.log_exists()
        if log_exists == False:
            return redirect('/createLog')
        else:
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


            return render_template('dashboard.html', user=user, local_time=local_time, log=log_exists, meals=meals, workout_count=workout_count)



def settings():
    if not 'user_id' in session.keys():
        return redirect('/')
    else:
        user = User.query.get(session['user_id'])
        user_feet = int(float(user.height) / float(12))
        user_inches = int(float(user.height) % float(12))
        return render_template('settings.html', user=user, user_feet=user_feet, user_inches=user_inches)

def updateSettings():
    if not 'user_id' in session.keys():
        return redirect('/')
    else:
        valid_settings = User.validate_settings(request.form)
        if valid_settings:
            user = User.query.get(session['user_id'])
            user.height = float((12 * int(request.form['feet'])) + int(request.form['inches']))
            user.weight = float(request.form['weight'])
            user.daily_calories = float(request.form['daily_calories'])
            db.session.commit()
            flash('User Information has been successfully updated!', 'success_msg')
        return redirect('/settings')


