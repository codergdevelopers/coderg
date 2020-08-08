from flask import Blueprint, render_template, session, redirect, url_for

from coderg.models import Project, User, Post

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route("/about/")
def about():
    return render_template("about.html",)


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

    # return render_template('lisu.html')


@main.route("/projects/")
def display_projects():
    categories = set()
    projects = Project.query.filter_by().all()

    # Getting all the available categories
    for project in projects:
        categories.add(project.category)

    return render_template("projects.html", categories=list(categories), projects=projects)


#      THIS IS TO ADD PROJECTS IN DATABASE
#      SHOULD BE RUN ONLY ONE TIME ON THE WEBSITE
#
#
# @main.route("/addprojects")
# def add_projects():
#     proj = Project(category="Python", title="Healthy programmer.", language='Python', purpose="Reminder for resting eyes, drink water and do some exercise at regular interval of time. Have pause feature", working_on="Advanced pause and snooze", link=r'https://github.com/aqdasak/Healthy-Programmer', author='Aqdas Ahmad Khan')
#     db.session.add(proj)
#     db.session.commit()
#
#
#     proj = Project(category="Python", title="Hey soldier prettify my folder", language='Python', purpose='Batch rename files in a given folder. Can ignore files', working_on="Using wildcards in ignore list", link=r'https://github.com/aqdasak/Batch-Rename', author='Aqdas Ahmad Khan')
#     db.session.add(proj)
#     db.session.commit()
#
#     proj = Project(category="Java", title="Starke", language='Java', purpose='Greeting message on startup', working_on="Logic based printing of characters", link=r'https://github.com/deepanshdubey/starke', author='Aqdas Ahmad Khan (+Deepansh Dubey)')
#     db.session.add(proj)
#     db.session.commit()
#
#     proj = Project(category="Java", title="MorseCode_Decoder", language='Java', purpose='Decoding the characters of Morse Code', working_on="Identifying user inputs", link=r'https://github.com/deepanshdubey/MorseCode_Decoder', author='Deepansh Dubey')
#     db.session.add(proj)
#     db.session.commit()
#
#     proj = Project(category="WEB - D", title="Coderg Frontend", language='HTML, CSS & JS', purpose='Building a website for our society', working_on="HTML, CSS & JS", link=r'https://github.com/deepanshdubey/Coderg', author='Deepansh Dubey')
#     db.session.add(proj)
#     db.session.commit()
#
#     proj = Project(category="WEB - D", title="Coderg Backend", language='Python (flask)',
#                     purpose='Backend of this website', working_on="Blogs section",
#                     link=r'https://github.com/codergdevelopers/coderg', author='Aqdas Ahmad Khan')
#     db.session.add(proj)
#     db.session.commit()
#
#     proj = Project(category="WEB - D", title="React.calc", language='Javascript', purpose='Basic four function calculator', working_on="ReactJS", link=r'https://github.com/deepanshdubey/react.calc.git', author='Deepansh Dubey')
#     db.session.add(proj)
#     db.session.commit()
#
#     return "New post added"
#
#
