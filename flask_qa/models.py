from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from .extensions import db

# This class is from the original file
# Removing this affects auth.py
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(100))
    expert = db.Column(db.Boolean)
    admin = db.Column(db.Boolean)


class UserDb(db.Model):
    fullname = db.Column(db.String(), nullable=False)
    username = db.Column(db.String(), primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    admin = db.Column(db.Boolean, default=False)

class Projects(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(), unique=False, nullable=False)
    title = db.Column(db.String(), unique=True, nullable=False)
    language = db.Column(db.String(), unique=False, nullable=False)
    purpose = db.Column(db.String(), unique=False, nullable=False)
    working_on = db.Column(db.String(), unique=False, nullable=False)
    link = db.Column(db.String(), unique=False, nullable=False)
    author = db.Column(db.String(), unique=False, nullable=False)

class PostDb(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    tagline = db.Column(db.String(), nullable=False)
    username = db.Column(db.String(), nullable=False)
    fullname = db.Column(db.String(), nullable=False)
    slug = db.Column(db.String(), unique=True, nullable=False)
    content = db.Column(db.String(), nullable=False)
    date = db.Column(db.String(), nullable=True)
    img_file = db.Column(db.String(), nullable=True)
# author is the username of the user
# name should be fetched from UserDb

