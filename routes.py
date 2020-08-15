from config import app
from controllers import *

app.add_url_rule('/', view_func=home)