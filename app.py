from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

def Get_Posts(board):
    posts = Posts.query.filter(Posts.board == board).all()
    return posts

@app.route("/")
def Show_Index():
    boards = Boards.query.order_by(Boards.acronym.desc()).all()
    return render_template('index.html', boards = boards)

@app.route("/boards/<string:acronym>")
def Board_View(acronym):
    posts = Get_Posts(acronym)
    return render_template('board.html', posts = posts)

if __name__ == "__main__":
    app.run(debug = True)


