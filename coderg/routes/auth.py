from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash

from coderg.extensions import db
from coderg.models import User, Role
from config.config import params
from coderg.util import check_role

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
            return redirect(url_for('auth.login'))

    return render_template('lisu.html')


@auth.route('/logout/')
def logout():
    session.pop('user')
    return redirect(url_for('auth.login'))


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


@auth.route('/setrole/', methods=['GET', 'POST'])
def setrole():
    if check_role('ADMIN'):
        roles_avl = params['roles']

        if request.method == 'POST':
            username = request.form.get('username')
            user = User.query.filter_by(username=username).first()
            new_roles = []

            # getting roles from html form
            for i in range(len(roles_avl)):
                role = request.form.get('role' + str(i + 1))
                new_roles.append(role)

            for role in roles_avl:
                # new role added
                if role in new_roles and role not in user.role:
                    db.session.add(Role(title=role, username=username))
                    db.session.commit()

                # role removed
                elif role not in new_roles and role in user.role:
                    for role_obj in user._user_role:
                        if role_obj.title == role:
                            db.session.delete(role_obj)
                            db.session.commit()

        users = User.query.all()
        return render_template('setrole.html', users=users, roles_avl=roles_avl)

    return redirect(url_for('main.index'))
