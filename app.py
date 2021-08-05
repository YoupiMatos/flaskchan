from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db =SQLAlchemy(app)

class  Boards(db.Model):
     id = db.Column(db.Integer, primary_key = True)


@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/bonjour")
def bonjour():
    return "<p>Bonjour.</p>"

if __name__ == "__main__":
    app.run(debug = True)