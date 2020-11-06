"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post, Tag, PostTag
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
def home():
    """render home page"""
    posts = Post.query.all()
    return render_template("home.html", posts=posts)

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
    posts = Post.query.filter(Post.user_id == user_id)
    return render_template("user-details.html", user=user, posts=posts)

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

    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")


@app.route("/users/<int:user_id>/posts/new", methods=["GET"])
def new_post_form(user_id):
    """Form to add new post."""

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template("new-post.html", user=user, tags=tags)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_post(user_id):
    """Adds new post and redirects to user page."""
    # user = User.query.get_or_404(user_id)
    
    title = request.form['title']
    content = request.form['content']
    tags = request.form.getlist("tags")

    post = Post(title=title, content=content, user_id=user_id)
    for tag in tags:
        tag_obj = Tag.query.get_or_404(tag)
        post.tags.append(tag_obj)
    
    db.session.add(post)
    db.session.commit()
    return redirect(f"/users/{user_id}")


@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """Displays post"""

    
    post = Post.query.get_or_404(post_id)
    user = post.user
    tags = post.tags
    return render_template("post-detail.html", post=post, user=user, tags=tags)


@app.route("/posts/<int:post_id>/edit", methods=["GET"])
def edit_post_form(post_id):
    """Form to add new post."""

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    tag_ids = [tag.id for tag in post.tags]
    return render_template("edit-post.html", post=post, tags=tags, tag_ids=tag_ids)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    """Edits a post and redirects back to post page."""

    title = request.form['title']
    content = request.form['content']
    tags = request.form.getlist("tags")

    post = Post.query.get_or_404(post_id)
    post.title = title
    post.content = content
    for tag in tags:
        tag_obj = Tag.query.get_or_404(tag)
        post.tags.append(tag_obj)

    db.session.add(post)
    db.session.commit()
    return redirect(f"/posts/{post_id}")


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Deletes a user and redirects to user list."""
    post = Post.query.get_or_404(post_id)
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    return redirect(f"/users/{post.user_id}")

@app.route("/tags")
def list_tags():
    """List tags and link add form."""

    tags = Tag.query.all()
    return render_template("tag-list.html", tags=tags)

@app.route("/tags/<int:tag_id>")
def show_tag(tag_id):
    """Show posts associated with a tag."""

    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts
    return render_template("tag.html", tag=tag, posts=posts)

@app.route("/tags/new", methods=["GET"])
def new_tag_form():
    """Form to add a new tag."""

    return render_template("new-tag.html")

@app.route("/tags/new", methods=["POST"])
def add_tag():
    """Creates a new tag."""

    name = request.form['name']
    tag = Tag(name=name)

    db.session.add(tag)
    db.session.commit()
    return redirect("/tags")

@app.route("/tags/<int:tag_id>/edit", methods=["GET"])
def edit_tag_form(tag_id):
    """Form to edit a tag."""

    tag = Tag.query.get_or_404(tag_id)
    return render_template("edit-tag.html", tag=tag)


@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_tag(tag_id):
    """Edits a tag and redirects back to tag page."""

    name = request.form['name']

    tag = Tag.query.get_or_404(tag_id)
    tag.name = name

    db.session.add(tag)
    db.session.commit()
    return redirect(f"/tags/{tag_id}")

@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """Deletes a tag and redirects to tag list."""

    tag = Tag.query.get_or_404(tag_id)
    Tag.query.filter_by(id=tag_id).delete()
    db.session.commit()
    return redirect("/tags")