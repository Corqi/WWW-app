from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user


bp = Blueprint('bp_choose', __name__)


@bp.route('/choose')
@login_required
def select_character_get():
    return render_template('choose.html')