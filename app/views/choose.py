from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from ..app import db
from ..decorators import check_confirmed

bp = Blueprint('bp_choose', __name__)


@bp.route('/choose')
@login_required
@check_confirmed
def choose_get():
    if current_user.character_type == 0:
        return render_template('choose.html')
    return redirect(url_for('bp_game.character_get'))


@bp.route('/choose/<character_no>')
@login_required
@check_confirmed
def select_character(character_no):
    if current_user.character_type == 0:
        try:
            character_no = int(character_no)
        except:
            return redirect(url_for("bp_choose.choose_get"))

        if 0 < character_no < 4:
            current_user.character_type = character_no
            db.session.commit()
            return redirect(url_for("bp_game.character_get"))

        return redirect(url_for("bp_choose.choose_get"))
    return redirect(url_for('bp_game.character_get'))
