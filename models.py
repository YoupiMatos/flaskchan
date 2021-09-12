from app import db
from datetime import datetime

class  Boards(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    acronym = db.Column(db.String, nullable = False, unique=True)
    description = db.Column(db.String)

# class Threads(db.Model):
    # pass

class Replies(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False, default="Anonyme")
    date = db.Column(db.DateTime, default = datetime.utcnow)
    content = db.Column(db.String, nullable = False)