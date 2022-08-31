from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user


bp = Blueprint('bp_shop', __name__)


@bp.route('/shop')
@login_required
def shop_get():
    return render_template('shop.html')