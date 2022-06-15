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
    subject = CharField(max_length=64, default='')
    name = CharField(max_length=40, default='Anonyme')
    date = DateTimeField(default = datetime.utcnow().strftime('%d/%m/%y - %H:%M:%S'))
    content = CharField(max_length=1200)

    @classmethod
    def getThreads(cls, searchedBoard):
        return Post.select().where((Post.board == searchedBoard) & (Post.op_id == 0)).order_by(Post.date.desc())

    @classmethod
    def getThreadsPosts(cls, searchedBoard, post_id):
        return Post.select().where((Post.board == searchedBoard) & (Post.op_id == post_id))

    @classmethod
    def getOp(cls, op_id):
        return Post.select().where(Post.id == op_id)