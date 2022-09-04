from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from ..app import db

bp = Blueprint('bp_choose', __name__)


@bp.route('/choose')
@login_required
def choose_get():
    if current_user.level == 0:
        return render_template('choose.html')
    return redirect(url_for('bp_game.character_get'))


@bp.route('/choose/<character_no>')
@login_required
def select_character(character_no):
    if current_user == 0:
        try:
            character_no = int(character_no)
        except:
            return redirect(url_for("bp_choose.choose_get"))

        if 0 < character_no < 4:
            current_user.level = character_no
            db.session.commit()
            return redirect(url_for("bp_game.character_get"))

        return redirect(url_for("bp_choose.choose_get"))
    return redirect(url_for('bp_game.character_get'))
