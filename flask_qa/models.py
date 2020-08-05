from werkzeug.security import generate_password_hash

from .extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullname = db.Column(db.String(), nullable=False)

    username = db.Column(db.String(), primary_key=True, unique=True, nullable=False)
    email = db.Column(db.String(), nullable=False)
    _hashed_password = db.Column(db.String(255), nullable=False, server_default='')

    admin = db.Column(db.Boolean, default=False)
    editor = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        return self._hashed_password

    @password.setter
    def password(self, unhashed_password):
        self._hashed_password = generate_password_hash(unhashed_password)


class Project(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(), unique=False, nullable=False)
    title = db.Column(db.String(), unique=True, nullable=False)
    language = db.Column(db.String(), unique=False, nullable=False)
    purpose = db.Column(db.String(), unique=False, nullable=False)
    working_on = db.Column(db.String(), unique=False, nullable=False)
    link = db.Column(db.String(), unique=False, nullable=False)
    author = db.Column(db.String(), unique=False, nullable=False)


class Post(db.Model):
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
# name should be fetched from User

