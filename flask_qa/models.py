from werkzeug.security import generate_password_hash

from .extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(), nullable=False)

    username = db.Column(db.String(), unique=True, nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    _hashed_password = db.Column(db.String(255), nullable=False, server_default='')

    _user_role = db.relationship('Role', backref='user_obj')
    post = db.relationship('Post', backref='author_obj')

    # admin = db.Column(db.Boolean, default=False)
    # editor = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        return self._hashed_password

    @password.setter
    def password(self, unhashed_password):
        self._hashed_password = generate_password_hash(unhashed_password)

    @property
    def role(self):
        # list comprehension to get all the roles in a list
        return [role_obj.name for role_obj in self._user_role]

    @role.setter
    def role(self, user_role):
        self._user_role = user_role


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # user_obj = ___ (pseudo column)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    tagline = db.Column(db.String(), nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # author_obj = ___ (pseudo column)

    # username = db.Column(db.String(), nullable=False)
    # fullname = db.Column(db.String(), nullable=False)
    slug = db.Column(db.String(), unique=True, nullable=False)
    content = db.Column(db.String(), nullable=False)
    date = db.Column(db.String(), nullable=True)
    img_file = db.Column(db.String(), nullable=True)

    @property
    def sno(self):
        return self.id

# author is the username of the user
# name should be fetched from User


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(), unique=False, nullable=False)
    title = db.Column(db.String(), unique=True, nullable=False)
    language = db.Column(db.String(), unique=False, nullable=False)
    purpose = db.Column(db.String(), unique=False, nullable=False)
    working_on = db.Column(db.String(), unique=False, nullable=False)
    link = db.Column(db.String(), unique=False, nullable=False)
    author = db.Column(db.String(), unique=False, nullable=False)
