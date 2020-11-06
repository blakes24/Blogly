"""Seed file to make sample data for blogly db."""

from models import db, User, Post, Tag, PostTag
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
frank = User(first_name='Doctor', last_name="Frankenstein")
count = User(first_name='Count', last_name="Dracula")
dorian = User(first_name='Dorian', last_name="Gray")

# Add new objects to session, so they'll persist
db.session.add(frank)
db.session.add(count)
db.session.add(dorian)

# Commit changes
db.session.commit()

alive = Post(title="It's Alive", content="I did it! I have created life!")
crazy = Tag(name="crazy")
arrogant = Tag(name="arrogant")
dangerous = Tag(name="dangerous")

alive.tags.append(crazy)
alive.tags.append(arrogant)
frank.posts.append(alive)

db.session.add(crazy)
db.session.add(arrogant)
db.session.add(dangerous)

db.session.add(frank)
db.session.commit()