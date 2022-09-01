from flask import Blueprint, render_template, redirect, url_for, request, flash, Markup
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user

from ..forms import LoginForm, RegisterForm

from ..app import db
from ..models import User, MissionHandler

bp = Blueprint('bp_auth', __name__)


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

        user = User.query.filter_by(name=name).first()
        if user:
            flash(Markup(f'Nickname already exists.'), 'error')
            return redirect(url_for('bp_auth.register_get'))

        new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        new_mission_handler = MissionHandler(user_id=new_user.id)
        db.session.add(new_mission_handler)
        db.session.commit()

        flash('Your account has been created you can now log in', 'info')
        return redirect(url_for('bp_auth.login_get'))

    return render_template('register.html', form=form)
