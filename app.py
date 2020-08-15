from flask import render_template, request, session, redirect, flash
from config import app, db 
from models import * 
import routes 

if __name__ == "__main__": 
    app.run(debug=True)