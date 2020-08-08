from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash

from flask_qa.extensions import db
from flask_qa.models import User

from config.config import params

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('uname').lower()
        password = request.form.get('pass')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user'] = username
            return redirect(url_for('main.dashboard'))
        else:
            flash('Could not login. Please check and try again.')
            return redirect(url_for('.login'))

    return render_template('lisu.html')


@auth.route('/logout')
def logout():
    session.pop('user')
    return redirect(url_for('main.dashboard'))


@auth.route("/signup/", methods=['GET', 'POST'])
def signup():
    # if user/admin already logged in
    # then redirect to home or dashboard
    if 'user' in session:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        fullname = request.form.get('fullname').title()
        username = request.form.get('uname').lower()
        email = request.form.get('email')
        password1 = request.form.get('pass1')
        password2 = request.form.get('pass2')

        error = None
        # checking against existing usernames and email
        if User.query.filter_by(email=email).first():
            error = 'Email already registered'
        elif User.query.filter_by(username=username).first():
            error = 'Username not available'
        else:
            if password1 == password2:
                user = User(fullname=fullname, username=username, email=email,
                            password=password1)
                db.session.add(user)
                db.session.commit()

                # TO DO flash in html and dashboard change checking
                flash("Sign up completed", "success")
                # signing in
                session['user'] = username
                return redirect(url_for('main.dashboard'))
            else:
                error = "Wrong values entered"
                # return redirect("/dashboard")

        flash(error, "danger")
        # return redirect("/dashboard")

    return redirect(url_for('main.dashboard'))
