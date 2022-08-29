from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from ..app import db
from ..models import User

bp = Blueprint('bp_game', __name__)


@bp.route('/game')
@login_required
def game_get():
    return render_template('game.html')


@bp.route('/settings')
@login_required
def settings_get():
    return render_template('settings.html')


@bp.route('/settings', methods=['POST'])
@login_required
def settings_post():
    if "name_submit" in request.form:

        if request.form.get('name') != "":
            current_user.name = request.form.get('name')
            db.session.commit()
            flash(f'Your nickname has been changed', 'name_info')
            return redirect(url_for('bp_game.settings_get'))

        flash(f'Incorrect nickname was given', 'name_error')
        return redirect(url_for('bp_game.settings_get'))

    if "email_submit" in request.form:
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()

        if user:
            flash(f'Email address already exists.', 'email_error')
            return redirect(url_for('bp_game.settings_get'))

        if email == "":
            flash(f'Email is incorrect', 'email_error')
            return redirect(url_for('bp_game.settings_get'))

        current_user.email = email
        db.session.commit()
        flash(f'Your email has been changed', 'email_info')
        return redirect(url_for('bp_game.settings_get'))

    if "password_submit" in request.form:
        password = request.form.get('password')
        new_password = request.form.get('new_password')

        if check_password_hash(current_user.password, password):
            current_user.password = generate_password_hash(new_password, method='sha256')
            db.session.commit()
            flash(f'Your password has been changed.', 'password_info')
            return redirect(url_for('bp_game.settings_get'))

        flash(f'The password you entered is incorrect', 'password_error')
        return redirect(url_for('bp_game.settings_get'))

@bp.route('/shop')
@login_required
def shop_get():
    return render_template('shop.html')


# Get list of messages
@bp.route('/game/s', methods=['GET'])
@login_required
def game_s_get():
    return render_template('game.html')