from datetime import datetime
from flask import Flask, request, render_template, flash, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from . import create_app, database
from .models import db, Todo

app = create_app()

# ========= REST ==========


@app.route("/api/v1/todo", methods=["GET"])
def index():
    todo_list = database.get_all(Todo, Todo.created_at)
    todos = []
    for todo in todo_list.all():
        todos.append({"id": todo.id,
                      "text": todo.text,
                      "done": todo.done,
                      "created_at": todo.created_at})
    return jsonify(todos)


@app.route("/api/v1/todo", methods=["POST"])
def add():
    if "text" in request.json:
        text = request.json.get("text")
        if text:
            database.add_instance(Todo, text=text)
            return "OK", 201
        return "Error: item text is empty!", 422
    return "Error: no 'text' in data!", 422


@app.route("/api/v1/todo/<int:id>", methods=["DELETE"])
def delete(id):
    count = database.delete_instance(Todo, id)
    if count:
        return "", 204
    return f"Error: item {id} does not exist!", 422


@app.route("/api/v1/todo/<int:id>/toggle_done", methods=["PATCH"])
def toggle_done(id):
    todo = database.get_instance(Todo, id)
    if todo:
        todo.done = not todo.done
        database.commit_changes()
        return "", 204
    return f"Error: item {id} does not exist!", 422


@app.route("/api/v1/todo/<int:id>", methods=["PATCH"])
def edit(id):
    if "text" in request.json:
        text = request.json.get("text")
        if text:
            count = database.edit_instance(Todo, id, text=text)
            if count:
                return f"OK", 200
            return f"Error: item {id} does not exist!", 422
        return "Error: item text is empty!", 422
    return "Error: no 'text' in data!", 422

# ========= HTML ==========


@app.route("/", methods=["GET"])
def index_html():
    todo_list = database.get_all(Todo, Todo.created_at)
    return render_template("index.html", todo_list=todo_list)


@app.route("/add", methods=["POST"])
def add_html():
    if "text" in request.form:
        text = request.form.get("text")
        if text:
            database.add_instance(Todo, text=text)
            flash("New todo is added")
        else:
            flash("Error: item text is empty!")
    else:
        flash("Error: no 'text' in data!")
    return redirect(url_for("index_html"))


@app.route("/delete/<int:id>", methods=["POST"])
def delete_html(id):
    count = database.delete_instance(Todo, id)
    if count:
        flash(f"Item {id} is deleted")
    else:
        flash(f"Error: item {id} does not exist!")
    return redirect(url_for("index_html"))


@app.route("/toggle_done/<int:id>", methods=["POST"])
def toggle_done_html(id):
    todo = database.get_instance(Todo, id)
    if todo:
        todo.done = not todo.done
        database.commit_changes()
    return redirect(url_for("index_html"))


@app.route("/edit_html/<int:id>", methods=["POST"])
def edit_html(id):
    if "text" in request.form:
        text = request.form["text"]
        count = database.edit_instance(Todo, id, text=text)
        if count:
            flash("Item is edited")
        else:
            flash("Error: no 'text' in data!")
    return redirect(url_for("index_html"))
