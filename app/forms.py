from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[InputRequired(message='E-mail field is required.'), Email()], id='inputEmail')
    password = PasswordField('Password', validators=[InputRequired(message='Password field is required.')], id='inputPassword')
    remember = BooleanField('Remember me')


class RegisterForm(FlaskForm):
    email = StringField('E-mail', validators=[InputRequired(message='E-mail field is required.'), Email()], id='inputEmail')
    name = StringField('Name', validators=[InputRequired(message='Name field is required.'), Length(min=3, max=7, message='Your name must be between 3 and 7 characters')])
    password = PasswordField('Password', validators=[InputRequired(message='Password field is required.'), Length(min=6, max=20, message='Your password is too short')], id='inputPassword')
    password_confirm = PasswordField('Confirm password', validators=[InputRequired(message='Password field is required.'), EqualTo('password', message='Passwords must be equal')], id='inputPasswordConfirm')


class ChangeEmailForm(FlaskForm):
    email = StringField('E-mail', validators=[InputRequired(message='E-mail field is required.'), Email()],
                        id='inputEmail')
    submit = SubmitField('Change e-mail', id="buttonChangeEmail")


class ChangePasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired(message='Password field is required.')],
                             id='inputPassword')
    new_password = PasswordField('New password', validators=[InputRequired(message='Password field is required.'), Length(min=6, max=20, message='Your new password is too short')],
                                 id='inputNewPassword')
    new_password_confirm = PasswordField('Confirm password',
                                         validators=[InputRequired(message='Password field is required.'),
                                                     EqualTo('new_password', message='Passwords must be equal')],
                                         id='inputPasswordConfirm')
    submit = SubmitField('Change password', id="buttonChangePassword")


class ChangeNameForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(message='Name field is required.'), Length(min=3, max=7, message='Your name must be between 3 and 7 characters')])
    submit = SubmitField('Change nickname', id="buttonChangeNickname")
