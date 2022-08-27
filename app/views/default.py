from flask import Blueprint, render_template, redirect, url_for, request

bp = Blueprint('bp_default', __name__)

@bp.route('/', methods=["POST", "GET"])
def default_get():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        print(email, password)
        return redirect(url_for("bp_game.game_get"))
    else:
        return render_template('default.html')