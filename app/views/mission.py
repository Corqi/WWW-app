import json

from flask import Blueprint, render_template, request, flash, redirect, url_for
from ..app import db
import datetime
from flask_login import login_required, current_user
from ..models import Mission, User, MissionHandler

bp = Blueprint('bp_mission', __name__)


@bp.route('/mission/<int:mission_type>')
@login_required
def set_mission(mission_type):
    mission_handler = MissionHandler.query.filter_by(user_id=current_user.id).first()
    if current_user.is_free == "true":
        current_user.is_free = "false"
        mission_handler.mission_picked_id = mission_type
        mission_handler.mission_taken_time = datetime.datetime.now()
        db.session.commit()

        if mission_type == 1:
            duration = mission_handler.easy_mission_duration
        elif mission_type == 2:
            duration = mission_handler.medium_mission_duration
        else:
            duration = mission_handler.hard_mission_duration

        start_time = mission_handler.mission_taken_time
        end_time = start_time + datetime.timedelta(seconds=duration)
        time_left = end_time - start_time
        time_left = time_left.total_seconds()

        return render_template('mission.html', duration=duration, time_left=time_left)

    else:
        m_type = mission_handler.mission_picked_id
        if m_type == 1:
            duration = mission_handler.easy_mission_duration
        elif m_type == 2:
            duration = mission_handler.medium_mission_duration
        else:
            duration = mission_handler.hard_mission_duration

        start_time = mission_handler.mission_taken_time
        end_time = start_time + datetime.timedelta(seconds=duration)

        if datetime.datetime.now() >= end_time:
            time_left = 0
        else:
            time_left = end_time - datetime.datetime.now()
            time_left = time_left.total_seconds()

        return render_template('mission.html', duration=duration, time_left=time_left)
