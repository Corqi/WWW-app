import datetime
import random

from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

from app.app import db
from app.decorators import selected_character_required, check_confirmed
from app.models import MissionHandler
from app.views.bar import calculate_damage_reduction

bp = Blueprint('bp_game', __name__)


@bp.route('/game')
@login_required
@selected_character_required
@check_confirmed
def game_get():
    if current_user.is_free == "false":
        return redirect(url_for('bp_mission.set_mission', mission_type=1))
    return render_template('game.html')


@bp.route('/character')
@login_required
@selected_character_required
@check_confirmed
def character_get():

    if datetime.datetime.now() < current_user.last_death_time + datetime.timedelta(seconds=30):
        return redirect(url_for('bp_death.get_death'))
    elif current_user.current_health <= 0:
        current_user.current_health = current_user.max_health
        db.session.commit()

    mission_handler = MissionHandler.query.filter_by(user_id=current_user.id).first()

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
                money_earned = mission_handler.easy_mission_cost
                random_damage = random.randint(0, 10)
            elif mission_handler.mission_picked_id == 2:
                money_earned = mission_handler.medium_mission_cost
                random_damage = random.randint(11, 20)
            else:
                money_earned = mission_handler.hard_mission_cost
                random_damage = random.randint(21, 30)

            damage_taken = random_damage - calculate_damage_reduction(random_damage)

            mission_handler.mission_picked_id = 0
            current_user.current_health -= damage_taken

            if current_user.current_health <= 0:
                current_user.last_death_time = datetime.datetime.now()
                db.session.commit()
                return redirect(url_for('bp_death.get_death'))

            current_user.money += money_earned
            db.session.commit()
            character = current_user
            return render_template("character.html", character=character, money_earned=money_earned,
                                   damage_taken=damage_taken)
        else:
            return redirect(url_for('bp_mission.set_mission', mission_type=1))

    character = current_user
    return render_template("character.html", character=character, money_earned=0,
                           damage_taken=0)

