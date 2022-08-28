from flask import Blueprint, render_template, request

bp = Blueprint('bp_game', __name__)

@bp.route('/game')
def game_get():
    return render_template('game.html')

# Get list of messages
@bp.route('/game/s', methods=['GET'])
def game_s_get():
    return render_template('game.html')