from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user


bp = Blueprint('bp_game', __name__)


@bp.route('/game')
@login_required
def game_get():
    return render_template('game.html')


@bp.route('/shop')
@login_required
def shop_get():
    return render_template('shop.html')


@bp.route('/bar')
@login_required
def bar_get():
    return render_template('bar.html')


@bp.route('/game/character')
@login_required
def character_get():
    from ..models import User
    character = User.query.get_or_404(1)
    return render_template("character.html", character=character)
