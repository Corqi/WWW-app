import random

from flask import Blueprint, render_template, request, flash, redirect, url_for
from ..app import db
import datetime
from flask_login import login_required, current_user
from ..models import Mission, User, MissionHandler
from ..decorators import selected_character_required

bp = Blueprint('bp_bar', __name__)


@bp.route('/bar')
@login_required
@selected_character_required
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

    if current_user.is_free == "false":
        start_time = mission_handler.mission_taken_time
        if mission_handler.mission_picked_id == 1:
            end_time = start_time + datetime.timedelta(seconds=mission_handler.easy_mission_duration)
        elif mission_handler.mission_picked_id == 2:
            end_time = start_time + datetime.timedelta(seconds=mission_handler.medium_mission_duration)
        else:
            end_time = start_time + datetime.timedelta(seconds=mission_handler.hard_mission_duration)

        # here player receives money and damage after completing mission
        if datetime.datetime.now() >= end_time:
            current_user.is_free = "true"
            if mission_handler.mission_picked_id == 1:
                current_user.money += mission_handler.easy_mission_cost
                random_damage = random.randint(0, 10)
            elif mission_handler.mission_picked_id == 2:
                current_user.money += mission_handler.medium_mission_cost
                random_damage = random.randint(11, 20)
            else:
                current_user.money += mission_handler.hard_mission_cost
                random_damage = random.randint(21, 30)

            current_user.current_health -= random_damage - calculate_damage_reduction(random_damage)
            mission_handler.mission_picked_id = 0
            db.session.commit()
        else:
            return redirect(url_for('bp_mission.set_mission', mission_type=1))

    if (current_user.is_free == "true" and time_difference.total_seconds()/60 > 1
        and mission_handler.mission_picked_id == 0)\
            or current_user.is_free == "true":
        mission_handler.mission_picked_id = 0
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

        random_easy_cost = random.randint(5, 10)
        random_medium_cost = random.randint(10, 14)
        random_hard_cost = random.randint(16, 22)
        easy_cost_increase = calculate_cost_increase(random_easy_cost)
        medium_cost_increase = calculate_cost_increase(random_medium_cost)
        hard_cost_increase = calculate_cost_increase(random_hard_cost)
        mission_handler.easy_mission_cost = random_easy_cost + easy_cost_increase
        mission_handler.medium_mission_cost = random_medium_cost + medium_cost_increase
        mission_handler.hard_mission_cost = random_hard_cost + hard_cost_increase

        random_easy_duration = random.randint(20, 30)
        random_medium_duration = random.randint(40, 60)
        random_hard_duration = random.randint(80, 120)
        easy_duration_reduction = calculate_duration_reduction(random_easy_duration)
        medium_duration_reduction = calculate_duration_reduction(random_medium_duration)
        hard_duration_reduction = calculate_duration_reduction(random_hard_duration)
        mission_handler.easy_mission_duration = random_easy_duration - easy_duration_reduction
        mission_handler.medium_mission_duration = random_medium_duration - medium_duration_reduction
        mission_handler.hard_mission_duration = random_hard_duration - hard_duration_reduction

        mission_handler.last_missions_update = datetime.datetime.now()

        db.session.commit()

    else:
        chosen_easy = Mission.query.filter_by(id=mission_handler.easy_mission_id).first()
        chosen_medium = Mission.query.filter_by(id=mission_handler.medium_mission_id).first()
        chosen_hard = Mission.query.filter_by(id=mission_handler.hard_mission_id).first()

        random_easy_cost = mission_handler.easy_mission_cost
        random_medium_cost = mission_handler.medium_mission_cost
        random_hard_cost = mission_handler.hard_mission_cost
        easy_cost_increase = calculate_cost_increase(random_easy_cost)
        medium_cost_increase = calculate_cost_increase(random_medium_cost)
        hard_cost_increase = calculate_cost_increase(random_hard_cost)

        random_easy_duration = mission_handler.easy_mission_duration
        random_medium_duration = mission_handler.medium_mission_duration
        random_hard_duration = mission_handler.hard_mission_duration
        easy_duration_reduction = calculate_duration_reduction(random_easy_duration)
        medium_duration_reduction = calculate_duration_reduction(random_medium_duration)
        hard_duration_reduction = calculate_duration_reduction(random_hard_duration)

    cost_dict = {
        "easy_cost": random_easy_cost,
        "easy_increase": easy_cost_increase,
        "medium_cost": random_medium_cost,
        "medium_increase": medium_cost_increase,
        "hard_cost": random_hard_cost,
        "hard_increase": hard_cost_increase
    }
    duration_dict = {
        "easy_duration": random_easy_duration,
        "easy_reduction": easy_duration_reduction,
        "medium_duration": random_medium_duration,
        "medium_reduction": medium_duration_reduction,
        "hard_duration": random_hard_duration,
        "hard_reduction": hard_duration_reduction
    }
    return render_template('bar.html', chosen_easy=chosen_easy,
                           chosen_medium=chosen_medium, chosen_hard=chosen_hard,
                           cost_dict=cost_dict, duration_dict=duration_dict)


def calculate_cost_increase(cost):
    cost_increase_factor = current_user.luck - 1
    return int(cost * 0.2 * cost_increase_factor)


def calculate_duration_reduction(duration):
    duration_reduction_factor = current_user.speed - 1
    return int(duration * 0.2 * duration_reduction_factor)


def calculate_damage_reduction(damage):
    damage_reduction_factor = current_user.armor - 1
    return int(damage * 0.15 * damage_reduction_factor)