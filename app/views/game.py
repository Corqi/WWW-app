from flask import Blueprint, render_template, request
from ..models import Message

bp = Blueprint('bp_game', __name__)

@bp.route('/game')
def game_get():
    return render_template('game.html')

# Get list of messages
@bp.route('/game/s', methods=['GET'])
def game_s_get():
    message = Message.query.get_or_404(4)
    print(message.content)

    return render_template('game.html')