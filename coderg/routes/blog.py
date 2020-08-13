import math

from flask import Blueprint, render_template, request, session, redirect, flash, url_for

from coderg.extensions import db
from coderg.models import Post, User
from config.config import params
from coderg.util import check_role

blog = Blueprint('blog', __name__)


@blog.route("/blog/")
def blog_index():
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


@blog.route("/post/<string:post_slug>", methods=['GET'])
def post_route(post_slug):
    # first(), if multiple post by same slug are found. We avoid it as it would be unique
    post = Post.query.filter_by(slug=post_slug).first()

    return render_template('post.html', post=post)


@blog.route("/edit/<string:sno>", methods=['GET', 'POST'])
def edit(sno):
    if 'user' in session:
        if request.method == 'POST':
            ntitle = request.form.get('title')
            ntagline = request.form.get('tline')
            nslug = request.form.get('slug')
            ncontent = request.form.get('content')
            nimg_file = request.form.get('img_file')

            # New post can be added by anyone logged in
            if sno == '0':
                post = Post(title=ntitle, tagline=ntagline, slug=nslug, content=ncontent, img_file=nimg_file,
                            author=session['user'])
                db.session.add(post)
                db.session.commit()
                flash("New post added", "success")
                return redirect(url_for('main.dashboard'))

            post = Post.query.filter_by(sno=sno).first()
            # Post can be edited by either admin or author
            if 'user' in session and (post.author.username == session['user'] or check_role('ADMIN')):
                post = Post.query.filter_by(sno=sno).first()
                post.title = ntitle
                post.tagline = ntagline
                post.slug = nslug
                post.content = ncontent
                post.img_file = nimg_file
                db.session.commit()
                flash("Edited successfully", "success")
                return redirect(url_for('main.dashboard'))

        post = Post.query.filter_by(sno=sno).first()
        if post or sno == '0':
            return render_template('edit.html', post=post, sno=sno)
        return redirect(url_for('main.dashboard'))

    return redirect(url_for('main.dashboard'))


@blog.route("/delete/<sno>", methods=['GET', 'POST'])
def delete(sno):
    if check_role('ADMIN'):
        post = Post.query.filter_by(sno=sno).first()
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted successfully", "success")

    if 'user' in session:
        post = Post.query.filter_by(sno=sno).first()
        if post and post.author.username == session['user']:
            db.session.delete(post)
            db.session.commit()
            flash("Post deleted successfully", "success")

    return redirect(url_for('main.dashboard'))
