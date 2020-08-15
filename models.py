from sqlalchemy.sql import func 
from config import db 
from flask import flash, request 

class User(db.Model):
    