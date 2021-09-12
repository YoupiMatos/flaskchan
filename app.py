from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db =SQLAlchemy(app)

@app.route("/")
def hello_world():
    boards = Boards.query.order_by(Boards.acronym.desc()).all()
    return render_template('index.html', boards = boards)

@app.route("/boards/<string:acronym>")
def board_view(acronym):
    return render_template('board.html')

@app.route("/bonjour")
def bonjour():
    return "<p>Bonjour.</p>"

if __name__ == "__main__":
    app.run(debug = True)