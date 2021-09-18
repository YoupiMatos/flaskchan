from app import db
from datetime import datetime

class Boards(db.Model):
    acronym = db.Column(db.String, nullable = False, unique = True, primary_key = True)
    name = db.Column(db.String, nullable = False)
    description = db.Column(db.String)

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    op_id = db.Column(db.Integer)
    board = db.Column(db.String)
    subject = db.Column(db.String)
    name = db.Column(db.String, default="Anonyme")
    date = db.Column(db.DateTime, default = datetime.utcnow)
    content = db.Column(db.String, nullable = False)