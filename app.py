from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

def Get_Boards():
    boards = Boards.query.order_by(Boards.acronym.asc()).all()
    return boards

def Get_Posts(board):
    posts = Posts.query.filter(Posts.board == board).all()
    return posts

@app.route("/")
def Show_Index():
    boards = Get_Boards()
    return render_template('index.html', boards = boards)

@app.route("/boards/<string:acronym>", methods = ['POST', 'GET'])
def Board_View(acronym):
    if request.method == 'POST':
        subject = request.form['subject']
        if request.form['name']:
            name = request.form['name']
        content = request.form['content']
        if 'name' in locals():
            new_post = Posts(op_id = 0, board = acronym, subject = subject, name = name, content = content )
        else:
            new_post = Posts(op_id = 0, board = acronym, subject = subject, content = content )
        
        try:
            db.session.add(new_post)
            db.session.commit()
            return redirect('/boards/' + acronym)
        except:
            return "Erreur lors de l'ajout du post"
    else:
        posts = Get_Posts(acronym)
        boards = Get_Boards()
        return render_template('board.html', posts = posts, boards = boards, current_board = acronym)

if __name__ == "__main__":
    app.run(debug = True)


