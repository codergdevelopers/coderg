from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from .extensions import db 

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(100))
    expert = db.Column(db.Boolean)
    admin = db.Column(db.Boolean)

    # questions_asked = db.relationship(
    #     'Question',
    #     foreign_keys='Question.asked_by_id',
    #     backref='asker',
    #     lazy=True
    # )
    #
    # answers_requested = db.relationship(
    #     'Question',
    #     foreign_keys='Question.expert_id',
    #     backref='expert',
    #     lazy=True
    # )

    @property
    def unhashed_password(self):
        raise AttributeError('Cannot view unhashed password!')

    @unhashed_password.setter
    def unhashed_password(self, unhashed_password):
        self.password = generate_password_hash(unhashed_password)

class Projects(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(), unique=False, nullable=False)
    title = db.Column(db.String(), unique=True, nullable=False)
    language = db.Column(db.String(), unique=False, nullable=False)
    purpose = db.Column(db.String(), unique=False, nullable=False)
    working_on = db.Column(db.String(), unique=False, nullable=False)
    link = db.Column(db.String(), unique=False, nullable=False)
    author = db.Column(db.String(), unique=False, nullable=False)