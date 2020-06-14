from datetime import datetime
from flask import Flask, request, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from . import create_app, database
from .models import db, Todo

app = create_app()


@app.route("/")
def index():
    todo_list = database.get_all(Todo, Todo.created_at)
    return render_template("index.html", todo_list=todo_list)


@app.route("/add", methods=["POST"])
def add():
    if "text" in request.form:
        text = request.form["text"]
        database.add_instance(Todo, text=text)
        flash("New todo is added")
    else:
        flash("Error: no 'text' in data!")
    return redirect(url_for("index"))


@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    database.delete_instance(Todo, id)
    flash(f"Item {id} is deleted")
    return redirect(url_for("index"))


@app.route("/toggle_done/<int:id>", methods=["POST"])
def toggle_done(id):
    todo = database.get_instance(Todo, id)
    todo.done = not todo.done
    database.edit_instance(Todo, id)
    return redirect(url_for("index"))

@app.route("/edit/<int:id>", methods=["POST"])
def edit(id):
    if "text" in request.form:
        text = request.form["text"]
        database.edit_instance(Todo, id, text=text)
        flash("Item is edited")
    else:
        flash("Error: no 'text' in data!")
    return redirect(url_for("index"))
