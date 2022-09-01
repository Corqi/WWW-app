import random

from flask import Blueprint, render_template, request, flash, redirect, url_for
from ..app import db
import datetime
from flask_login import login_required, current_user
from ..models import Mission, User, MissionHandler

bp = Blueprint('bp_bar', __name__)


@bp.route('/bar')
@login_required
def bar_get():
    # obj1 = Mission(title="misjalatwa1", content="ale mega prosta", danger_level=1)
    # obj2 = Mission(title="misjasrednia1", content="ale mega srednia", danger_level=2)
    # obj3 = Mission(title="misjatrudna1", content="ale mega trudna", danger_level=3)
    # db.session.add(obj1)
    # db.session.add(obj2)
    # db.session.add(obj3)
    # db.session.commit()

    mission_handler = MissionHandler.query.filter_by(user_id=current_user.id).first()

    last_missions_update = mission_handler.last_missions_update
    time_difference = datetime.datetime.now() - last_missions_update

    if time_difference.total_seconds()/60 > 1:
        easy_missions = Mission.query.filter_by(danger_level=1).all()
        medium_missions = Mission.query.filter_by(danger_level=2).all()
        hard_missions = Mission.query.filter_by(danger_level=3).all()

        chosen_easy = random.choice(easy_missions)
        chosen_medium = random.choice(medium_missions)
        chosen_hard = random.choice(hard_missions)

        mission_handler.last_missions_update = datetime.datetime.now()
        mission_handler.easy_mission_id = chosen_easy.id
        mission_handler.medium_mission_id = chosen_medium.id
        mission_handler.hard_mission_id = chosen_hard.id

        mission_handler.easy_mission_cost = random.randint(5, 10)
        mission_handler.medium_mission_cost = random.randint(10, 14)
        mission_handler.hard_mission_cost = random.randint(16, 22)

        mission_handler.easy_mission_duration = random.randint(20, 30)
        mission_handler.medium_mission_duration = random.randint(40, 60)
        mission_handler.hard_mission_duration = random.randint(80, 120)

        mission_handler.last_missions_update = datetime.datetime.now()

        db.session.commit()

        return render_template('bar.html', chosen_easy=chosen_easy,
                               chosen_medium=chosen_medium, chosen_hard=chosen_hard,
                               mission_handler=mission_handler)
    else:
        chosen_easy = Mission.query.filter_by(id=mission_handler.easy_mission_id).first()
        chosen_medium = Mission.query.filter_by(id=mission_handler.medium_mission_id).first()
        chosen_hard = Mission.query.filter_by(id=mission_handler.hard_mission_id).first()

        return render_template('bar.html', chosen_easy=chosen_easy,
                               chosen_medium=chosen_medium, chosen_hard=chosen_hard,
                               mission_handler=mission_handler)

