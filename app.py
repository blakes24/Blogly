"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

@app.route("/")
def to_users():
    """redirect to user list"""

    return redirect("/users")

@app.route("/users")
def list_users():
    """List users and link add form."""

    users = User.query.all()
    return render_template("list.html", users=users)

@app.route("/users/new", methods=["GET"])
def new_user_form():
    """Form to add new user."""

    return render_template("new-user.html")

@app.route("/users/new", methods=["POST"])
def add_user():
    """Adds new user and redirects to user list."""
    first_name = request.form['first-name']
    last_name = request.form['last-name']
    image_url = request.form['image-url']
    
    image_url = image_url if image_url else None

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()
    return redirect(f"/users/{user.id}")

@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show info on a user."""

    user = User.query.get_or_404(user_id)
    return render_template("details.html", user=user)

@app.route("/users/<int:user_id>/edit")
def edit_user_form(user_id):
    """Show form to edit user info."""

    user = User.query.get_or_404(user_id)
    return render_template("edit-user.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    """Edits user and redirects to user list."""

    first_name = request.form['first-name']
    last_name = request.form['last-name']
    image_url = request.form['image-url']
    
    image_url = image_url if image_url else None

    user = User.query.get_or_404(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.add(user)
    db.session.commit()
    return redirect("/users")

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Deletes a user and redirects to user list."""

    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect("/users")