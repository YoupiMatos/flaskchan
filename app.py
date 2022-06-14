import os.path
from flask import Flask, render_template, url_for, request, redirect
from peewee import *
from playhouse.flask_utils import FlaskDB, get_object_or_404
from datetime import datetime
from models import *

# Configuration
APP_DIR = os.path.dirname(os.path.realpath(__file__))
DATABASE = 'sqliteext:///%s' % os.path.join(APP_DIR, 'flaskchan.db')

# Flask app configuration using the values up there
app = Flask(__name__)
app.config.from_object(__name__)

# Database configuration using peewee util FlaskDB
flask_db = FlaskDB(app)
db = flask_db.database

def Get_Posts(board):
    posts = Post.query.filter(Post.board == board).all()
    return posts

@app.route("/")
def Show_Index():
    boards = Board.getBoards()
    return render_template('index.html', boards = boards)

@app.route("/boards/<string:acronym>", methods = ['POST', 'GET'])
def Board_View(acronym):
    """ if request.method == 'POST':
        subject = request.form['subject']
        if request.form['name']:
            name = request.form['name']
        content = request.form['content']
        if 'name' in locals():
            new_post = Post(op_id = 0, board = acronym, subject = subject, name = name, content = content )
        else:
            new_post = Post(op_id = 0, board = acronym, subject = subject, content = content )
        
        try:
            db.session.add(new_post)
            db.session.commit()
            return redirect('/boards/' + acronym)
        except:
            return "Erreur lors de l'ajout du post"
    else: """
    current_board = get_object_or_404(Board.getCurrentBoard(acronym))
    posts = Post.getPosts(acronym)
    boards = Board.getBoards()
    return render_template('board.html', posts = posts, boards = boards, current_board = current_board)

def main():
    db.create_tables([Board, Post], safe=True)

if __name__ == "__main__":
    main()
    app.run(debug = True)