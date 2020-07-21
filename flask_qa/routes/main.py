from flask import Blueprint, render_template, request, session, redirect, flash

from flask_qa.models import Projects, UserDb, PostDb
from flask_qa.extensions import db

from config.config import params
from hashlib import sha256

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html',)


@main.route("/about")
def about():
    return render_template("about.html", params=params)


@main.route("/contact")
def contact():
    return render_template("contact.html")


# @main.route("/lisu")
# def lisu():
#     return render_template("lisu.html")


@main.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    # admin already logged in
    if 'user' in session and session['user'] == params["admin_user"]:
        posts = PostDb.query.all()
        return render_template('dashboard.html', params=params, posts=posts)

    # user already logged in
    if 'user' in session:
        posts = PostDb.query.filter_by(author=session['user'])
        return render_template('dashboard.html', params=params, posts=posts)

    # logging in
    if request.method == 'POST':
        username = request.form.get('uname')
        password = request.form.get('pass')
        password = sha256(password.encode('utf-8')).hexdigest()
        # admin
        if username == params["admin_user"] and password == params["admin_password"]:
            # Log in & Redirect to admin panel
            session['user'] = username
            posts = PostDb.query.all()
            return render_template('dashboard.html', params=params, posts=posts)

        # user
        user = UserDb.query.filter_by(username=username).first()
        if user:
            if password == user.password:
                session['user'] = username
                posts = PostDb.query.filter_by(author=username)
                return render_template('dashboard.html', params=params, posts=posts)
            else:
                flash("Wrong password", "danger")

        else:
            flash(username + " does not have account", "danger")

    return render_template('lisu.html', params=params)


@main.route("/signup", methods=['GET','POST'])
def signup():
    # user/admin already logged in
    if 'user' in session:
        return redirect("/dashboard")

    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('uname')
        password1 = request.form.get('pass1')
        password2 = request.form.get('pass2')
        # checking against existing usernames
        user = UserDb.query.filter_by(username=username).first()
        if not user:
            if password1 == password2:
                user = UserDb(name=name, username=username, password=sha256(password1.encode('utf-8')).hexdigest())
                db.session.add(user)
                db.session.commit()

                # TO DO flash in html and dashboard change checking
                flash("Sign up completed", "success")
                # signing in
                session['user'] = username
                return redirect("/dashboard")
            else:
                flash("Wrong values entered", "danger")
                return redirect("/dashboard")

        else:
            flash("Username not available", "danger")
            return redirect("/dashboard")

    return redirect("/dashboard")



@main.route("/projects")
def display_projects():
    categories = set()
    projects = Projects.query.filter_by().all()

    # Getting all the available categories
    for project in projects:
        categories.add(project.category)

    return render_template("projects.html", categories=list(categories), projects=projects)


@main.route("/blog")
def blog():
    return render_template("blog.html")




#      THIS IS TO ADD PROJECTS IN DATABASE
#      SHOULD BE RUN ONLY ONE TIME ON THE WEBSITE
#
#
# @main.route("/addprojects")
# def add_projects():
#     proj = Projects(category="Python", title="Healthy programmer.", language='Python', purpose="Reminder for resting eyes, drink water and do some exercise at regular interval of time. Have pause feature", working_on="Advanced pause and snooze", link=r'https://github.com/aqdasak/Healthy-Programmer', author='Aqdas Ahmad Khan')
#     db.session.add(proj)
#     db.session.commit()
#
#
#     proj = Projects(category="Python", title="Hey soldier prettify my folder", language='Python', purpose='Batch rename files in a given folder. Can ignore files', working_on="Using wildcards in ignore list", link=r'https://github.com/aqdasak/Batch-Rename', author='Aqdas Ahmad Khan')
#     db.session.add(proj)
#     db.session.commit()
#
#     proj = Projects(category="Java", title="Starke", language='Java', purpose='Greeting message on startup', working_on="Logic based printing of characters", link=r'https://github.com/deepanshdubey/starke', author='Aqdas Ahmad Khan (+Deepansh Dubey)')
#     db.session.add(proj)
#     db.session.commit()
#
#     proj = Projects(category="Java", title="MorseCode_Decoder", language='Java', purpose='Decoding the characters of Morse Code', working_on="Identifying user inputs", link=r'https://github.com/deepanshdubey/MorseCode_Decoder', author='Deepansh Dubey')
#     db.session.add(proj)
#     db.session.commit()
#
#     proj = Projects(category="WEB - D", title="Coderg Frontend", language='HTML, CSS & JS', purpose='Building a website for our society', working_on="HTML, CSS & JS", link=r'https://github.com/deepanshdubey/Coderg', author='Deepansh Dubey')
#     db.session.add(proj)
#     db.session.commit()
#
#     proj = Projects(category="WEB - D", title="Coderg Backend", language='Python (flask)',
#                     purpose='Backend of this website', working_on="Blogs section",
#                     link=r'https://github.com/codergdevelopers/coderg', author='Aqdas Ahmad Khan')
#     db.session.add(proj)
#     db.session.commit()
#
#     proj = Projects(category="WEB - D", title="React.calc", language='Javascript', purpose='Basic four function calculator', working_on="ReactJS", link=r'https://github.com/deepanshdubey/react.calc.git', author='Deepansh Dubey')
#     db.session.add(proj)
#     db.session.commit()
#
#     return "New post added"
#
#
