from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user


bp = Blueprint('bp_select_character', __name__)


@bp.route('/select_character')
@login_required
def select_character_get():
    return render_template('select_character.html')