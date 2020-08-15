from flask import render_template, redirect, request, flash, session
from config import db 
from models import *

# render home page
def home():
    return render_template('index.html')