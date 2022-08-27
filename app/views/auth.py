from flask import Blueprint, render_template

bp = Blueprint('bp_auth', __name__)

@bp.route('/')
def login_get():
    return render_template('login.html')

@bp.route('/register')
def register_get():
    return render_template('register.html')