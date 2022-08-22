from flask import Blueprint, render_template

bp = Blueprint('bp_default', __name__)

@bp.route('/')
def default_get():
    return render_template('default.html')