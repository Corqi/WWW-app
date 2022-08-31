from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, EqualTo

from ..app import db
from ..models import User


bp = Blueprint('bp_settings', __name__)


class ChangeEmailForm(FlaskForm):
    email = StringField('E-mail', validators=[InputRequired(message='E-mail field is required.'), Email()], id='inputEmail')
    submit = SubmitField('Change e-mail', id="buttonChangeEmail")


class ChangePasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired(message='Password field is required.')],
                             id='inputPassword')
    new_password = PasswordField('New password', validators=[InputRequired(message='Password field is required.')],
                             id='inputNewPassword')
    new_password_confirm = PasswordField('Confirm password',
                                     validators=[InputRequired(message='Password field is required.'),
                                                 EqualTo('new_password', message='Passwords must be equal')],
                                     id='inputPasswordConfirm')
    submit = SubmitField('Change password', id="buttonChangePassword")


class ChangeNameForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(message='Name field is required.')])
    submit = SubmitField('Change nickname', id="buttonChangeNickname")
    

@bp.route('/settings')
@login_required
def settings_get():
    name_form = ChangeNameForm()
    email_form = ChangeEmailForm()
    password_form = ChangePasswordForm()

    return render_template('settings.html', name_form=name_form, email_form=email_form, password_form=password_form)


@bp.route('/settings/name', methods=['POST'])
def change_name():
    name_form = ChangeNameForm()

    if name_form.validate_on_submit():
        print(name_form.errors)
        # TODO check if there is the same nickname in db
        if name_form.name.data != current_user.name:
            current_user.name = name_form.name.data
            db.session.commit()
            flash(f'Your nickname has been changed', 'name_info')
            return redirect(url_for('bp_settings.settings_get'))

        flash(f'Same nickname was given', 'name_error')
        return redirect(url_for('bp_settings.settings_get'))

    for item in name_form.errors.values():
        flash(*item, 'name_error')
    return redirect(url_for('bp_settings.settings_get'))


@bp.route('/settings/email', methods=['POST'])
def change_email():
    email_form = ChangeEmailForm()

    if email_form.validate_on_submit():
        print(email_form.errors)
        user = User.query.filter_by(email=email_form.email.data).first()

        if user:
            flash(f'Email address already exists.', 'email_error')
            return redirect(url_for('bp_settings.settings_get'))

        current_user.email = email_form.email.data
        db.session.commit()
        flash(f'Your email has been changed', 'email_info')
        return redirect(url_for('bp_settings.settings_get'))

    for item in email_form.errors.values():
        flash(*item, 'email_error')
    return redirect(url_for('bp_settings.settings_get'))


@bp.route('/settings/password', methods=['POST'])
def change_password():
    password_form = ChangePasswordForm()

    if password_form.validate_on_submit():
        if check_password_hash(current_user.password, password_form.password.data):
            current_user.password = generate_password_hash(password_form.new_password.data, method='sha256')
            db.session.commit()
            flash(f'Your password has been changed.', 'password_info')
            return redirect(url_for('bp_settings.settings_get'))

        flash(f'The password you entered is incorrect', 'password_error')
        return redirect(url_for('bp_settings.settings_get'))

    for item in password_form.errors.values():
        flash(*item, 'password_error')
    return redirect(url_for('bp_settings.settings_get'))