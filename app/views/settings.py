from flask import Blueprint, render_template, session, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from ..forms import ChangeNameForm, ChangeEmailForm, ChangePasswordForm

from ..app import db
from ..models import User

from ..decorators import selected_character_required, is_free_true_required, is_alive_required, check_confirmed

bp = Blueprint('bp_settings', __name__)


@bp.route('/settings')
@login_required
@selected_character_required
@is_alive_required
@check_confirmed
def settings_get():
    if current_user.is_free == "false":
        return redirect(url_for('bp_mission.set_mission', mission_type=1))

    name_form = ChangeNameForm()
    email_form = ChangeEmailForm()
    password_form = ChangePasswordForm()

    return render_template('settings.html', name_form=name_form, email_form=email_form, password_form=password_form)


@bp.route('/settings/name', methods=['POST'])
@login_required
@selected_character_required
@is_alive_required
@check_confirmed
def change_name():
    if current_user.is_free == "false":
        return redirect(url_for('bp_mission.set_mission', mission_type=1))

    name_form = ChangeNameForm()

    if name_form.validate_on_submit():
        if name_form.name.data != current_user.name:
            user = User.query.filter_by(name=name_form.name.data).first()
            if user:
                session.pop('_flashes', None)
                flash(f'Nickname already exists.', 'name_error')
                return redirect(url_for('bp_settings.settings_get'))

            current_user.name = name_form.name.data
            db.session.commit()
            session.pop('_flashes', None)
            flash(f'Your nickname has been changed', 'name_info')
            return redirect(url_for('bp_settings.settings_get'))

        session.pop('_flashes', None)
        flash(f'Same nickname was given', 'name_error')
        return redirect(url_for('bp_settings.settings_get'))

    for item in name_form.errors.values():
        session.pop('_flashes', None)
        flash(*item, 'name_error')
    return redirect(url_for('bp_settings.settings_get'))


@bp.route('/settings/email', methods=['POST'])
@login_required
@selected_character_required
@is_free_true_required
@is_alive_required
@check_confirmed
def change_email():

    email_form = ChangeEmailForm()

    if email_form.validate_on_submit():
        print(email_form.errors)
        user = User.query.filter_by(email=email_form.email.data).first()

        if user:
            session.pop('_flashes', None)
            flash(f'Email address already exists.', 'email_error')
            return redirect(url_for('bp_settings.settings_get'))

        current_user.email = email_form.email.data
        db.session.commit()
        session.pop('_flashes', None)
        flash(f'Your email has been changed', 'email_info')
        return redirect(url_for('bp_settings.settings_get'))

    for item in email_form.errors.values():
        session.pop('_flashes', None)
        flash(*item, 'email_error')
    return redirect(url_for('bp_settings.settings_get'))


@bp.route('/settings/password', methods=['POST'])
@login_required
@selected_character_required
@is_free_true_required
@is_alive_required
@check_confirmed
def change_password():

    password_form = ChangePasswordForm()

    if password_form.validate_on_submit():
        if check_password_hash(current_user.password, password_form.password.data):
            current_user.password = generate_password_hash(password_form.new_password.data, method='sha256')
            db.session.commit()
            session.pop('_flashes', None)
            flash(f'Your password has been changed.', 'password_info')
            return redirect(url_for('bp_settings.settings_get'))

        session.pop('_flashes', None)
        flash(f'The password you entered is incorrect', 'password_error')
        return redirect(url_for('bp_settings.settings_get'))

    for item in password_form.errors.values():
        session.pop('_flashes', None)
        flash(*item, 'password_error')
    return redirect(url_for('bp_settings.settings_get'))