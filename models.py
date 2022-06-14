from peewee import *
from app import flask_db
from datetime import datetime

class Board(flask_db.Model):
    acronym = CharField(unique = True, primary_key = True)
    name = CharField()
    description = CharField()

    @classmethod
    def getBoards(cls):
        return Board.select()

    @classmethod
    def getCurrentBoard(cls, acronym):
        return Board.select().where(Board.acronym == acronym)

class Post(flask_db.Model):
    op_id = IntegerField()
    board = ForeignKeyField(Board, backref='posts')
    subject = CharField(max_length=64, null=True)
    name = CharField(max_length=40, default='Anonyme')
    date = DateTimeField(default = datetime.utcnow)
    content = CharField(max_length=1200)

    @classmethod
    def getPosts(cls, searchedBoard):
        return Post.select().where(Post.board == searchedBoard)