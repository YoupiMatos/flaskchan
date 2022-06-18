import os.path
from flask import Flask, render_template, url_for, request, redirect, flash, get_flashed_messages
from playhouse.flask_utils import FlaskDB, get_object_or_404
from datetime import datetime
from werkzeug.utils import secure_filename
from models import *

# Configuration
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
APP_DIR = os.path.dirname(os.path.realpath(__file__))
DATABASE = 'sqliteext:///%s' % os.path.join(APP_DIR, 'flaskchan.db')
SECRET_KEY = 'shhh, secret!'

# Flask app configuration using the values up there
app = Flask(__name__)
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = APP_DIR + '/static/uploads'

# Database configuration using peewee util FlaskDB
flask_db = FlaskDB(app)
db = flask_db.database

@app.route("/")
def showIndex():
    boards = Board.getBoards()
    return render_template('index.html', boards = boards)

@app.route("/boards/<acronym>", methods = ['POST', 'GET'])
def boardView(acronym):
    if request.method == 'POST':
        post = Post()
        post.op_id = 0
        post.subject = request.form.get('subject')
        post.board = Board.select().where(Board.acronym == acronym)
        if request.form.get('name'): post.name = request.form.get('name')
        if request.form.get('content'):
            post.content = request.form.get('content')
            if post.content.strip() == '':
                flash("Le contenu ne doit pas être vide.")
        else: flash("Le contenu ne doit pas être vide.")
        try:
            with db.atomic():
                if 'image' in request.files and request.files['image'].filename != '':
                    if request.files['image']:
                        filename = secure_filename(request.files['image'].filename)
                        request.files['image'].save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        post.image = request.files['image'].filename
                else: post.image = None
                post.save()

        except:
            flash("Erreur lors de l'ajout du post", 'error')
        else:
            flash('Post enregistré!', 'success')
            return redirect('/boards/' + acronym)

    current_board = get_object_or_404(Board.getCurrentBoard(acronym))
    posts = Post.getThreads(acronym)
    for post in posts:
        post.previews = Post.getLastReplies(post.id)
    boards = Board.getBoards()
    return render_template('board.html', posts = posts, boards = boards, current_board = current_board)


@app.route("/boards/<acronym>/<thread_id>", methods = ['GET', 'POST'])
def threadView(acronym, thread_id):
    if request.method == 'POST':
        reply = Post()
        reply.op_id = thread_id
        reply.board = Board.select().where(Board.acronym == acronym)
        if request.form.get('name'): reply.name = request.form.get('name')
        reply.content = request.form.get('content')
        try:
            with db.atomic():
                if 'image' in request.files and request.files['image'].filename != '':
                    if request.files['image']:
                        filename = secure_filename(request.files['image'].filename)
                        request.files['image'].save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        reply.image = request.files['image'].filename
                else: reply.image = None
                reply.save()
        except: flash("Erreur lors de l'ajout du post", "error")
        else:
            flash("Réponse enregistrée!", "success")
            return redirect('/boards/' + acronym + "/" + thread_id)


    current_board = get_object_or_404(Board.getCurrentBoard(acronym))
    op = get_object_or_404(Post.getOp(thread_id))
    posts = Post.getThreadsPosts(acronym, thread_id)
    boards = Board.getBoards()
    return render_template('thread.html', op = op, boards = boards, posts = posts, current_board = current_board)

def main():
    db.create_tables([Board, Post], safe=True)

if __name__ == "__main__":
    main()
    app.run(debug = True)