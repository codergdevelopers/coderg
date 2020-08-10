from flask import Blueprint, render_template, session, redirect, url_for

from coderg.models import Project, User, Post

from config.config import params
from coderg.util import check_role, role_required

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


# @role_required('ADMIN', redirect_to='/dashboard')
@main.route("/about/")
def about():
    return render_template("about.html", )


# @role_required('ADMIN','EDITOR')
@main.route("/contact/")
def contact():
    return render_template("contact.html")


@main.route("/dashboard/", methods=['GET', 'POST'])
def dashboard():
    # admin already logged in
    if check_role('ADMIN'):
        posts = Post.query.all()
        return render_template('dashboard.html', posts=posts)

    # user already logged in
    elif 'user' in session:
        posts = User.query.filter_by(username=session['user']).first().post
        return render_template('dashboard.html', posts=posts)

    # if 'user' not in session:
    else:
        return redirect(url_for('auth.login'))


# @role_required('EDITOR')
@main.route("/projects/")
def display_projects():
    categories = params['project_categories']
    projects = Project.query.all()
    return render_template("projects.html", categories=categories, projects=projects)
