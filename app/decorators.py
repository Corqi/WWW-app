from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user


def selected_character_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        if current_user.character_type == 0:
            return redirect(url_for('bp_choose.choose_get'))
        return f(*args, **kwargs)
    return function


def is_free_true_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        if current_user.is_free == "false":
            return redirect(url_for('bp_mission.set_mission', mission_type=1))
        return f(*args, **kwargs)
    return function


def is_alive_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        if current_user.current_health <= 0:
            return redirect(url_for('bp_death.get_death'))
        return f(*args, **kwargs)
    return function


def check_confirmed(f):
    @wraps(f)
    def function(*args, **kwargs):
        if current_user.confirmed is False:
            return redirect(url_for('bp_auth.unconfirmed'))
        return f(*args, **kwargs)

    return function

