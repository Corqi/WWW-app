from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

bp = Blueprint('bp_game', __name__)

@bp.route('/game')
@login_required
def game_get():
    return render_template('game.html')

# Get list of messages
@bp.route('/game/s', methods=['GET'])
@login_required
def game_s_get():
    return render_template('game.html')