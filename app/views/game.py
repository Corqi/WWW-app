from flask import Blueprint, render_template, request
# from flask_security import login_required
from ..app import db

bp = Blueprint('bp_game', __name__)

@bp.route('/game')
def default_get():
    return render_template('game.html')

# Get list of messages
# @bp.route('/game/s', methods=['GET'])
# def game_s_get():
#     message = Message.query.get_or_404(4)
#     print(message.content)

    # return render_template('game.html')

@bp.route('/game/character')
# @login_required
def character_get():
    from ..models import User
    # obj = User(email="www.wp2@wp.pl", password="asda", name="Grzegorz")
    # db.session.add(obj)
    # db.session.commit()
    character = User.query.get_or_404(1)
    return render_template("character.html", character=character)
