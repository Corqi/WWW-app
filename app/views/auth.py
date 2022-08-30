from flask import Blueprint, render_template, redirect, url_for, request, flash, Markup
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, EqualTo

import re

from ..app import db
from ..models import User


bp = Blueprint('bp_auth', __name__)


class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[InputRequired(message='E-mail field is required.'), Email()], id='inputEmail')
    password = PasswordField('Password', validators=[InputRequired(message='Password field is required.')], id='inputPassword')
    remember = BooleanField('Remember me')


class RegisterForm(FlaskForm):
    email = StringField('E-mail', validators=[InputRequired(message='E-mail field is required.'), Email()], id='inputEmail')
    name = StringField('Name', validators=[InputRequired(message='Name field is required.')])
    password = PasswordField('Password', validators=[InputRequired(message='Password field is required.')], id='inputPassword')
    password_confirm = PasswordField('Confirm password', validators=[InputRequired(message='Password field is required.'), EqualTo('password', message='Passwords must be equal')], id='inputPasswordConfirm')


@bp.route('/', methods=['POST', 'GET'])
def login_get():

    if current_user.is_authenticated:
        return redirect(url_for("bp_game.game_get"))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember = form.remember.data

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.', 'error')
            return redirect(url_for('bp_auth.login_get'))

        login_user(user, remember=remember)
        return redirect(url_for('bp_game.game_get'))
    else:
        return render_template('login.html', form=form)


@bp.route('/logout')
def logout_get():
    logout_user()
    flash("You've been successfully logged out.", 'info')
    return redirect(url_for('bp_auth.login_get'))


@bp.route('/register', methods=['POST', 'GET'])
def register_get():
    if current_user.is_authenticated:
        return redirect(url_for("bp_game.game_get"))

    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        name = form.name.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        if user:
            flash(Markup(f'Email address already exists. Go to <a href="{url_for("bp_auth.login_get")}">login page</a>.'),
                  'error')
            return redirect(url_for('bp_auth.register_get'))

        new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()

        flash('Your account has been created you can now log in', 'info')
        return redirect(url_for('bp_auth.login_get'))

    return render_template('register.html', form=form)
