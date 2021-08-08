from flask import Blueprint, render_template, redirect, url_for,  request
from flask_login import login_user, logout_user, login_required, current_user
from project.users import User, create_user

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():

    # code to validate and add user to database goes here
    username = request.form.get('username')
    user = User.get(username)
    if not user:
        user = create_user(username)
    login_user(user)

    return redirect(url_for('main.favorites'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
