from flask import Blueprint, render_template, redirect, url_for, request, flash, Markup
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user

from ..app import db
from ..models import User


bp = Blueprint('bp_auth', __name__)


@bp.route('/')
def login_get():
    if current_user.is_authenticated:
        return redirect(url_for("bp_game.game_get"))
    else:
        return render_template('login.html')


@bp.route('/', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    remember = False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.', 'error')
        return redirect(url_for('bp_auth.login_get'))

    login_user(user, remember=remember)
    return redirect(url_for('bp_game.game_get'))


@bp.route('/logout')
def logout_get():
    logout_user()
    flash("You've been successfully logged out.", 'info')
    return redirect(url_for('bp_auth.login_get'))


@bp.route('/register')
def register_get():
    if current_user.is_authenticated:
        return redirect(url_for("bp_game.game_get"))
    else:
        return render_template('register.html')


@bp.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    if email == "" or name == "" or password == "":
        flash('The data provided is incorrect', 'error')
        return redirect(url_for('bp_auth.register_get'))

    user = User.query.filter_by(email=email).first()

    if user:
        flash(Markup(f'Email address already exists. Go to <a href="{url_for("bp_auth.login_get")}">login page</a>.'), 'error')
        return redirect(url_for('bp_auth.register_get'))

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('bp_auth.login_get'))
