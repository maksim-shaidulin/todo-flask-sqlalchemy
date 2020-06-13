from datetime import datetime
from flask import Flask, request, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Secret Key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(250), nullable=False)
    done = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return f"{text}"


@app.route("/")
def index():
    todo_list = Todo.query.all()
    return render_template("index.html", todo_list=todo_list)

@app.route("/add", methods=["Post"])
def add():
    text = request.form["text"]
    db.session.add(Todo(text))
    db.session.commit()
    flash("New todo is added")
    return redirect(url_for("index"))

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    item = Todo.query.get(id)
    db.session.delete(item)
    db.session.commit()
    flash(f"Item {id} is deleted")
    return redirect(url_for("index"))

@app.route("/toggle_done/<int:id>", methods=["POST"])
def toggle_done(id):
    item = Todo.query.get(id)
    item.done = not item.done
    db.session.add(item)
    db.session.commit()
    return redirect(url_for("index"))
