import json

from flask import Blueprint, render_template, request, flash, redirect, url_for
from ..app import db
import datetime
from flask_login import login_required, current_user
from ..models import Mission, User, MissionHandler
from ..decorators import selected_character_required, is_free_true_required, check_confirmed

bp = Blueprint('bp_death', __name__)


@bp.route('/death')
@login_required
@selected_character_required
@is_free_true_required
@check_confirmed
def get_death():
    if current_user.current_health <= 0:
        duration = 30
        death_time = current_user.last_death_time
        end_time = death_time + datetime.timedelta(seconds=duration)

        if datetime.datetime.now() >= end_time:
            time_left = 0
        else:
            time_left = end_time - datetime.datetime.now()
            time_left = time_left.total_seconds()

        return render_template('death.html', duration=duration, time_left=time_left)
    else:
        return redirect(url_for('bp_game.character_get'))


