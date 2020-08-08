from flask_qa.models import Project, User, Post, Role
from flask_qa.extensions import db


def setPost():
    pass


def getPost():
    pass


def setUser():
    pass


def getUser():
    pass


def setRole():
    user = User.query.filter_by(username='check').first()
    role = Role(name='admin', user_obj=user)
    # user.role='admin'
    db.session.add(role)
    db.session.commit()