from flask import Blueprint, render_template, session, redirect, url_for

from coderg.models import Project, User, Post

from config.config import params
from coderg.util import check_role

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route("/about/")
def about():
    return render_template("about.html", )


@main.route("/contact/")
def contact():
    return render_template("contact.html")


@main.route("/dashboard/", methods=['GET', 'POST'])
def dashboard():
    # admin already logged in
    if check_role('ADMIN'):
        posts = Post.query.all()
        return render_template('dashboard.html', posts=posts, admin=True)

    # user already logged in
    elif 'user' in session:
        posts = User.query.filter_by(username=session['user']).first().post
        return render_template('dashboard.html', posts=posts, admin=False)

    # if 'user' not in session:
    else:
        return redirect(url_for('auth.login'))


@main.route("/projects/")
def display_projects():
    categories = params['project_categories']
    projects = Project.query.all()
    return render_template("projects.html", categories=categories, projects=projects)
