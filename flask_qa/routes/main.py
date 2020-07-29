from flask import Blueprint, render_template, request, session, redirect, flash

from flask_qa.models import Projects, UserDb, PostDb
from flask_qa.extensions import db

from config.config import params
from hashlib import sha256
from datetime import datetime
import math

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route("/about/")
def about():
    return render_template("about.html", params=params)


@main.route("/contact/")
def contact():
    return render_template("contact.html")


# @main.route("/lisu")
# def lisu():
#     return render_template("lisu.html")


@main.route("/dashboard/", methods=['GET', 'POST'])
def dashboard():
    # admin already logged in
    if 'user' in session and (session['user'] == params["admin"]["user1"] or session['user'] == params["admin"]["user2"]):
        posts = PostDb.query.all()
        return render_template('dashboard.html', params=params, posts=posts)

    # user already logged in
    if 'user' in session:
        posts = PostDb.query.filter_by(username=session['user'])
        return render_template('dashboard.html', params=params, posts=posts)

    # logging in
    if request.method == 'POST':
        username = request.form.get('uname').lower()
        password = request.form.get('pass')
        password = sha256(password.encode('utf-8')).hexdigest()
        # admin
        if (username == params["admin"]["user1"] and password == params["admin"]["password1"]) or username == params["admin"]["user2"] and password == params["admin"]["password2"]:
            # Log in & Redirect to admin panel
            session['user'] = username
            posts = PostDb.query.all()
            return render_template('dashboard.html', params=params, posts=posts)

        # user
        user = UserDb.query.filter_by(username=username).first()
        if user:
            if password == user.password:
                session['user'] = username
                posts = PostDb.query.filter_by(username=username)
                return render_template('dashboard.html', params=params, posts=posts)
            else:
                flash("Wrong password", "danger")

        else:
            flash(username + " does not have account", "danger")

    return render_template('lisu.html', params=params)


@main.route("/logout/")
def logout():
    session.pop('user')
    return redirect("/dashboard")


@main.route("/signup/", methods=['GET', 'POST'])
def signup():
    # user/admin already logged in
    if 'user' in session:
        return redirect("/dashboard")

    if request.method == 'POST':
        fullname = request.form.get('fullname').title()
        username = request.form.get('uname').lower()
        password1 = request.form.get('pass1')
        password2 = request.form.get('pass2')
        # checking against existing usernames
        user = UserDb.query.filter_by(username=username).first()
        if not user:
            if password1 == password2:
                user = UserDb(fullname=fullname, username=username,
                              password=sha256(password1.encode('utf-8')).hexdigest())
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


@main.route("/projects/")
def display_projects():
    categories = set()
    projects = Projects.query.filter_by().all()

    # Getting all the available categories
    for project in projects:
        categories.add(project.category)

    return render_template("projects.html", categories=list(categories), projects=projects)


@main.route("/blog/")
def blog():
    posts = PostDb.query.filter_by().all()
    last = math.ceil(len(posts) / int(params["no_of_posts"]))

    page = request.args.get('page')
    if not str(page).isnumeric():
        page = 1
    page = int(page)

    posts = posts[(page - 1) * int(params['no_of_posts']):(page - 1) * int(params['no_of_posts']) + int(
        params['no_of_posts'])]

    if page == 1 and page == last:
        prev = '#'
        next = '#'
    elif page == 1:
        prev = '#'
        next = '/blog/?page=' + str(page + 1)
    elif page == last:
        prev = '/blog/?page=' + str(page - 1)
        next = '#'
    else:
        prev = '/blog/?page=' + str(page - 1)
        next = '/blog/?page=' + str(page + 1)

    return render_template("blog.html", posts=posts, params=params, prev=prev, next=next)


@main.route("/post/<string:post_slug>", methods=['GET'])
def post_route(post_slug):
    post = PostDb.query.filter_by(
        slug=post_slug).first()  # first(), if multiple post by same slug are found. We avoid it as it would be unique

    return render_template('post.html', params=params, post=post)


@main.route("/edit/<string:sno>", methods=['GET', 'POST'])
def edit(sno):
    if 'user' in session:
        if request.method == 'POST':
            ntitle = request.form.get('title')
            ntagline = request.form.get('tline')
            nslug = request.form.get('slug')
            ncontent = request.form.get('content')
            nimg_file = request.form.get('img_file')

            # New post can be added by anyone logged in
            fullname = (UserDb.query.filter_by(username=session['user']).first()).fullname
            if sno == '0':
                post = PostDb(title=ntitle, tagline=ntagline, slug=nslug, content=ncontent, img_file=nimg_file,
                              username=session['user'], fullname=fullname,
                              date=datetime.now().strftime("%a %d %b %Y"))
                db.session.add(post)
                db.session.commit()
                flash("New post added", "success")
                return redirect("/dashboard")

            post = PostDb.query.filter_by(sno=sno).first()
            # Post can be edited by either admin or author
            if session['user'] == params["admin"]["user1"] or session['user'] == params["admin"]["user2"] or session['user'] == post.username:
                post = PostDb.query.filter_by(sno=sno).first()
                post.title = ntitle
                post.tagline = ntagline
                post.slug = nslug
                post.content = ncontent
                post.img_file = nimg_file
                db.session.commit()
                flash("Edited successfully", "success")
                return redirect("/dashboard")

        post = PostDb.query.filter_by(sno=sno).first()
        if post or sno == '0':
            return render_template('edit.html', params=params, post=post, sno=sno)
        return redirect("/dashboard")

    return redirect("/dashboard")


@main.route("/delete/<string:sno>", methods=['GET', 'POST'])
def delete(sno):
    if 'user' in session and session['user'] == params["admin"]["user1"] or session['user'] == params["admin"]["user2"]:
        post = PostDb.query.filter_by(sno=sno).first()
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted successfully", "success")

    if 'user' in session:
        post = PostDb.query.filter_by(sno=sno).first()
        if post and post.username == session['user']:
            db.session.delete(post)
            db.session.commit()
            flash("Post deleted successfully", "success")

    return redirect("/dashboard")

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
