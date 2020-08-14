from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash

from coderg.extensions import db, mail
from coderg.models import User
from config.config import params
from coderg.util import change_role, role_required

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


@auth.route('/role/', methods=['GET', 'POST'])
@role_required('ADMIN')
def role():
    roles_avl = params['roles']

    if request.method == 'POST':
        username = request.form.get('username')

        # getting roles from html form
        new_roles = []
        for i in range(len(roles_avl)):
            n_role = request.form.get('role' + str(i + 1))
            new_roles.append(n_role)

        change_role(username, *new_roles)

    users = User.query.all()
    return render_template('role.html', users=users, roles_avl=roles_avl)


@auth.route('/change-pass/', methods=['GET', 'POST'])
def change_pass():
    if 'user' in session:
        user = User.query.filter_by(username=session['user']).first()
        if request.method == 'POST':

            current_password = request.form.get('current_password')
            new_password1 = request.form.get('new_password1')
            new_password2 = request.form.get('new_password2')
            if check_password_hash(user.password, current_password):
                if new_password1 == new_password2:
                    user.password = new_password1
                    db.session.commit()
                    flash("Password changed successfully", "success")
                else:
                    flash("Password didn't match", "danger")

            else:
                flash('Current password is wrong', 'danger')

        return render_template('change_pass.html', user=user)

    return redirect(url_for('main.index'))


@auth.route('/reset-pass/', methods=['GET', 'POST'])
def reset_pass():
    if request.method == 'POST':

        otp = request.form.get('otp')

        user = request.form.get('user')
        new_password1 = request.form.get('new_password1')
        new_password2 = request.form.get('new_password2')

        # user = User.query.filter_by(email=email).first()
        if otp == session['otp']:
            session.pop('otp')
            if new_password1 == new_password2:
                user.password = new_password1
                db.session.commit()
                flash("Password changed successfully", "success")
            else:
                flash("Password didn't match", "danger")

        else:
            flash('OTP is wrong', 'danger')
        return redirect(url_for('auth.login'))


@auth.route('/reset_pass_otp', methods=['GET', 'POST'])
def reset_pass_otp():
    if request.method == 'POST':

        username = request.form.get('username')
        if username:
            user = User.query.filter_by(username=username).first()
        else:
            email = request.form.get('email')
            user = User.query.filter_by(email=email).first()
        if not user:
            flash(r"Username/email not found", 'danger')
            return render_template('forgot_pass/send_otp.html')

        from random import randint
        session['otp'] = randint(100000, 999999)
        
        return str(list(str(user.email), session['otp']))

        mail.send_message('Password reset: Coderg',
                          sender='noreply.coderg@gmail.com',
                          recipients=list(str(user.email)),
                          body=f'Hi {user.fullname},\n'
                               f'You recently requested to rest your password for Coderg account.\n'
                               f'This is your otp for password resetting\n{session["otp"]}\n\n'
                               f'If you did not request a password reset, please ignore this email.\n\n'
                               f'Thanks\nCoderg Developers\n{params["website_url"]}')

        return render_template('forgot_pass/reset_pass.html', user=user)

    return render_template('forgot_pass/send_otp.html')
