from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.decorators import selected_character_required


bp = Blueprint('bp_game', __name__)


@bp.route('/game')
@login_required
@selected_character_required
def game_get():
    if current_user.is_free == "false":
        return redirect(url_for('bp_mission.set_mission', mission_type=1))
    return render_template('game.html')


@bp.route('/character')
@login_required
@selected_character_required
def character_get():
    if current_user.is_free == "false":
        return redirect(url_for('bp_mission.set_mission', mission_type=1))
    character = current_user
    return render_template("character.html", character=character)
