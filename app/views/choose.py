from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from ..app import db

bp = Blueprint('bp_choose', __name__)

@bp.route('/choose')
@login_required
def game_get():
    if current_user.is_free == "false":
        return redirect(url_for('bp_mission.set_mission', mission_type=1))
    return render_template('game.html')