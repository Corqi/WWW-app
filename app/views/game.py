from flask import Blueprint, render_template

bp = Blueprint('bp_game', __name__)

@bp.route('/game')
def default_get():
    return render_template('game.html')