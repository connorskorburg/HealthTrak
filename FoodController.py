from flask import render_template, redirect, request, flash, session
from config import db 
from models import *
from datetime import datetime, timezone
from better_profanity import profanity
import requests
from secret import *

# get all meals in session for today
def meals():
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
            return redirect('/createLog')
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
        return redirect('/meals')


# render edit food page
def editFood(food_id):
    if not 'user_id' in session.keys():
        return redirect('/')
    else:
        log_exists = DailyLog.log_exists()
        if log_exists == False:
            return redirect('/createLog')
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
            return redirect('/createLog')
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
            return redirect('/createLog')


# food categories and exercise categories
def search():
    if not 'user_id' in session.keys():
        return redirect('/')
    else:
        log_exists = DailyLog.log_exists()
        if log_exists == False:
            return redirect('/createLog')
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
        log_exists = DailyLog.log_exists()
        if log_exists == False:
            return redirect('/createLog')
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
            for i in range(0,9):
                for y in result['foods'][i]['foodNutrients']:
                    if y['nutrientName'] == 'Total lipid (fat)':
                        fat = y['value']
                    if y['nutrientName'] == 'Carbohydrate, by difference':
                        carbs = y['value']
                    if y['nutrientName'] == 'Protein':
                        protein = y['value']
                results.append({
                    "id": i + 1,
                    "description":  result['foods'][i]['description'],
                    "protein":  protein,
                    "fat":  fat,
                    "carbs":  carbs,
                })
            return render_template('results.html', search=search, results=results)