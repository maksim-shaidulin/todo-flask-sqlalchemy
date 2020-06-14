from datetime import datetime
from flask import Flask, request, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from . import create_app
from .models import db, Todo

app = create_app()


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
