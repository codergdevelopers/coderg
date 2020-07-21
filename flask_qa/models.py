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


class Users(db.Model):
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String(30), unique=False, nullable=False)
    admin = db.Column(db.Boolean, default=True)

class Projects(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(), unique=False, nullable=False)
    title = db.Column(db.String(), unique=True, nullable=False)
    language = db.Column(db.String(), unique=False, nullable=False)
    purpose = db.Column(db.String(), unique=False, nullable=False)
    working_on = db.Column(db.String(), unique=False, nullable=False)
    link = db.Column(db.String(), unique=False, nullable=False)
    author = db.Column(db.String(), unique=False, nullable=False)

class Posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), unique=True, nullable=False)
    tagline = db.Column(db.String(40), unique=True, nullable=False)
    author = db.Column(db.String(20), unique=True, nullable=False)
    slug = db.Column(db.String(25), unique=True, nullable=False)
    content = db.Column(db.String(150), unique=True, nullable=False)
    date = db.Column(db.String(8), unique=True, nullable=True)
    img_file = db.Column(db.String(12), unique=True, nullable=True)
