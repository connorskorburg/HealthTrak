from config import app
from controllers import *

app.add_url_rule('/', view_func=index)
app.add_url_rule('/login', view_func=login, methods=['POST'])
app.add_url_rule('/register', view_func=register, methods=['POST'])
app.add_url_rule('/logout', view_func=logout)

app.add_url_rule('/meals', view_func=meals)
app.add_url_rule('/fooditem/new', view_func=newFood, methods=['POST'])
app.add_url_rule('/fooditem/edit/<int:food_id>', view_func=editFood)
app.add_url_rule('/updateFood', view_func=updateFood, methods=['POST'])

app.add_url_rule('/fitness', view_func=fitness)
app.add_url_rule('/workout/new', view_func=newWorkout, methods=['POST'])
app.add_url_rule('/exercise/new', view_func=newExercise, methods=['POST'])
app.add_url_rule('/workout/delete/<int:workout_id>', view_func=deleteWorkout)

app.add_url_rule('/fooditem/delete/<int:food_id>', view_func=deleteFood)

app.add_url_rule('/exercise/edit/<int:exercise_id>', view_func=editExercise)
app.add_url_rule('/updateExercise', view_func=updateExercise, methods=['POST'])
app.add_url_rule('/exercise/delete/<int:exercise_id>', view_func=deleteExercise)

app.add_url_rule('/calendar', view_func=showLog)

app.add_url_rule('/search', view_func=search, methods=['POST'])
app.add_url_rule('/searchResults', view_func=searchResults)

app.add_url_rule('/dashboard', view_func=dashboard)

app.add_url_rule('/settings', view_func=settings)
app.add_url_rule('/updateSettings', view_func=updateSettings, methods=['POST'])

app.add_url_rule('/reg', view_func=reg)

app.add_url_rule('/createLog', view_func=createLog)