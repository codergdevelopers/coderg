from datetime import datetime

from werkzeug.security import generate_password_hash

from .extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    fullname = db.Column(db.String(), nullable=False)
    username = db.Column(db.String(), unique=True, nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    _hashed_password = db.Column(
        db.String(255), nullable=False, server_default='')

    _user_role = db.relationship('Role', backref='user_obj')
    post = db.relationship('Post', backref='author_obj')

    @property
    def password(self):
        return self._hashed_password

    @password.setter
    def password(self, unhashed_password):
        self._hashed_password = generate_password_hash(unhashed_password)

    @property
    def role(self):
        # list comprehension to get a list of roles
        return {role_obj.title for role_obj in self._user_role}


class Role(db.Model):
    """
    FORMAT:
    Role(title=title_of_role, username=username_of_user)
    """
    id = db.Column(db.Integer, primary_key=True)
    _role_title = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # user_obj = ___ (pseudo column created by class 'User')

    @property
    def title(self):
        return self._role_title.upper()

    @title.setter
    def title(self, title1):
        self._role_title = title1.upper()

    @property
    def username(self):
        return self.user_obj.username

    @username.setter
    def username(self, username1):
        user = User.query.filter_by(username=username1).first()
        self.user_obj = user


class Post(db.Model):
    """
    FORMAT:
    Post(title=ntitle, tagline=ntagline, slug=nslug,
         content=ncontent, img_file=nimg_file, author=username)
    """
    sno = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(), nullable=False)
    tagline = db.Column(db.String(), nullable=False)
    slug = db.Column(db.String(), unique=True, nullable=False)
    content = db.Column(db.String(), nullable=False)
    img_file = db.Column(db.String(), nullable=True)

    date = db.Column(db.String(), nullable=True,
                     default=datetime.now().strftime("%a %d %b %Y"))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # author_obj = ___ (pseudo column created by class 'User')

    @property
    def author(self):
        # author(user) object from class 'User'
        return self.author_obj

    @author.setter
    def author(self, username1):
        # author is set by username
        user = User.query.filter_by(username=username1).first()
        self.author_obj = user


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), unique=True, nullable=False)
    language = db.Column(db.String(), unique=False, nullable=False)
    purpose = db.Column(db.String(), unique=False, nullable=False)
    working_on = db.Column(db.String(), unique=False, nullable=False)
    link = db.Column(db.String(), unique=False, nullable=False)
    author = db.Column(db.String(), unique=False, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('project_category.id'))

    category = db.relationship('Project_Category')


class Project_Category(db.Model):
    __tablename__ = 'project_category'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), unique=True, nullable=False)
