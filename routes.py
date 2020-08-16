from config import app
from controllers import *

app.add_url_rule('/', view_func=home)
app.add_url_rule('/dashboard', view_func=dashboard)
app.add_url_rule('/login', view_func=login, methods=['POST'])
app.add_url_rule('/register', view_func=register, methods=['POST'])
app.add_url_rule('/logout', view_func=logout)
app.add_url_rule('/mealtrack', view_func=mealtrack)
app.add_url_rule('/fooditem/new', view_func=newFood, methods=['POST'])