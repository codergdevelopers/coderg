from flask import Blueprint, render_template, session, redirect, url_for

from coderg.models import Project, User, Post
from config.config import params

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
    if 'user' in session and ('ADMIN' in User.query.filter_by(username=session['user']).first().role):
        posts = Post.query.all()
        return render_template('dashboard.html', posts=posts)

    # user already logged in
    elif 'user' in session:
        posts = User.query.filter_by(username=session['user']).first().post
        return render_template('dashboard.html', posts=posts)

    # if 'user' not in session:
    else:
        return redirect(url_for('auth.login'))


@main.route("/projects/")
def display_projects():
    # categories = set()

    categories = params['project_categories']
    projects = Project.query.filter_by().all()

    # Getting all the available categories
    # for project in projects:
    #     categories.add(project.category)

    return render_template("projects.html", categories=categories, projects=projects)
