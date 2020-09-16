from flask import render_template, redirect, request, flash, session
from config import db 
from models import *
from datetime import datetime, timezone
from better_profanity import profanity
import requests
from secret import *



#WORKOUT METHODS

# render template for adding workout/exercise
def fitness():
    if not 'user_id' in session.keys():
        return redirect('/')
    else:
        log_exists = DailyLog.log_exists()
        if log_exists == False:
            return redirect('/createLog')
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
        log_exists = DailyLog.log_exists()
        if log_exists == False:
            return redirect('/createLog')
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
            return redirect('/createLog')


#EXERCISE METHODS




# create exercise and add it to workout
def newExercise():
    if not 'user_id' in session.keys():
        return redirect('/')
    else:
        valid_ex = Exercise.valid_ex(request.form)
        log_exists = DailyLog.log_exists()
        if log_exists == False:
            return redirect('/createLog')
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
        log_exists = DailyLog.log_exists()
        if log_exists == False:
            return redirect('/createLog')
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
        return redirect('/createLog')
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
        if log_exists == False:
            return redirect('/createLog')
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