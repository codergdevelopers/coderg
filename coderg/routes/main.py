from flask import Blueprint, render_template, request, session, redirect, flash, url_for

from coderg.models import Project, User, Post, Role
from coderg.extensions import db

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


@main.route("/blog/")
def blog():
    posts = Post.query.filter_by().all()
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

    return render_template("blog.html", posts=posts, prev=prev, next=next)


@main.route("/post/<string:post_slug>", methods=['GET'])
def post_route(post_slug):
    # first(), if multiple post by same slug are found. We avoid it as it would be unique
    post = Post.query.filter_by(slug=post_slug).first()

    return render_template('post.html', post=post)


@main.route("/edit/<string:id>", methods=['GET', 'POST'])
def edit(id):
    if 'user' in session:
        if request.method == 'POST':
            ntitle = request.form.get('title')
            ntagline = request.form.get('tline')
            nslug = request.form.get('slug')
            ncontent = request.form.get('content')
            nimg_file = request.form.get('img_file')

            # New post can be added by anyone logged in
            if id == '0':
                post = Post(title=ntitle, tagline=ntagline, slug=nslug, content=ncontent, img_file=nimg_file,
                            author=session['user'])
                db.session.add(post)
                db.session.commit()
                flash("New post added", "success")
                return redirect(url_for('.dashboard'))

            post = Post.query.filter_by(id=id).first()
            # Post can be edited by either admin or author
            if session['user'] == params["admin"]["user1"] or session['user'] == params["admin"]["user2"] or session[
                'user'] == post.author.username:
                post = Post.query.filter_by(id=id).first()
                post.title = ntitle
                post.tagline = ntagline
                post.slug = nslug
                post.content = ncontent
                post.img_file = nimg_file
                db.session.commit()
                flash("Edited successfully", "success")
                return redirect(url_for('.dashboard'))

        post = Post.query.filter_by(id=id).first()
        if post or id == '0':
            return render_template('edit.html', post=post, id=id)
        return redirect(url_for('.dashboard'))

    return redirect(url_for('.dashboard'))


@main.route("/delete/<string:id>", methods=['GET', 'POST'])
def delete(id):
    if 'user' in session and session['user'] == params["admin"]["user1"] or session['user'] == params["admin"]["user2"]:
        post = Post.query.filter_by(id=id).first()
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted successfully", "success")

    if 'user' in session:
        post = Post.query.filter_by(id=id).first()
        if post and post.author.username == session['user']:
            db.session.delete(post)
            db.session.commit()
            flash("Post deleted successfully", "success")

    return redirect(url_for('.dashboard'))


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
