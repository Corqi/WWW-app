from flask import Blueprint, render_template, redirect, url_for, session, flash, Markup
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required

from ..forms import LoginForm, RegisterForm

from ..app import db
from ..models import User, MissionHandler

from ..token import generate_confirmation_token, confirm_token
from ..email import send_email


bp = Blueprint('bp_auth', __name__)


@bp.route('/', methods=['POST', 'GET'])
def login_get():
    if current_user.is_authenticated:
        return redirect(url_for('bp_game.character_get'))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember = form.remember.data

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            session.pop('_flashes', None)
            flash('Please check your login details and try again.', 'error')
            return redirect(url_for('bp_auth.login_get'))

        login_user(user, remember=remember)
        return redirect(url_for('bp_game.character_get'))
    else:
        return render_template('login.html', form=form)


@bp.route('/logout')
def logout_get():
    logout_user()
    session.pop('_flashes', None)
    flash("You've been successfully logged out.", 'info')
    return redirect(url_for('bp_auth.login_get'))


@bp.route('/register', methods=['POST', 'GET'])
def register_get():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        name = form.name.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if user:
            session.pop('_flashes', None)
            flash(Markup(f'Email address already exists. Go to <a href="{url_for("bp_auth.login_get")}">login page</a>.'),
                  'error')
            return redirect(url_for('bp_auth.register_get'))

        user = User.query.filter_by(name=name).first()
        if user:
            session.pop('_flashes', None)
            flash(Markup(f'Nickname already exists.'), 'error')
            return redirect(url_for('bp_auth.register_get'))

        new_user = User(
            email=email,
            name=name,
            password=generate_password_hash(password, method='sha256'),
            confirmed=False
        )

        token = generate_confirmation_token(new_user.email)
        confirm_url = url_for('bp_auth.confirm_email', token=token, _external=True)
        html = render_template('activate.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(new_user.email, subject, html)

        db.session.add(new_user)
        db.session.commit()

        new_mission_handler = MissionHandler(user_id=new_user.id)
        db.session.add(new_mission_handler)
        db.session.commit()

        session.pop('_flashes', None)
        if not current_user.is_authenticated:
            flash('Your account has been created you can now log in', 'info')
        return redirect(url_for('bp_auth.login_get'))

    return render_template('register.html', form=form)


@bp.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        session.pop('_flashes', None)
        flash('The confirmation link is invalid or has expired.', 'error')
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        session.pop('_flashes', None)
        flash('Account already confirmed. Please login.', 'info')
    else:
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
        session.pop('_flashes', None)
        flash('You have confirmed your account. Thanks!', 'info')
    return redirect(url_for('bp_auth.login_get'))


@bp.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect(url_for('bp_auth.login_get'))
    return render_template('unconfirmed.html')


@bp.route('/resend')
@login_required
def resend_confirmation():
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('bp_auth.confirm_email', token=token, _external=True)
    html = render_template('activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(current_user.email, subject, html)

    session.pop('_flashes', None)
    flash('A new confirmation email has been sent.', 'info')
    return redirect(url_for('bp_auth.unconfirmed'))
