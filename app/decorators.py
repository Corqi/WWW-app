from functools import wraps
from flask import redirect, url_for
from flask_login import current_user


def selected_character_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        if current_user.level == 0:
            return redirect(url_for('bp_choose.choose_get'))
        return f(*args, **kwargs)
    return function

