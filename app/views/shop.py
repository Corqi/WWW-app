from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user


bp = Blueprint('bp_shop', __name__)


class Cost():
    # TODO Write logic to calculate costs according to levels
    cost_dict = {'heal': 10, 'upgrade_weapon': 100, 'upgrade_armor': 1000, 'upgrade_ship': 0}

    def __init__(self):
        self.heal = self.cost_dict.get('heal')
        self.upgrade_weapon = self.cost_dict.get('upgrade_weapon')
        self.upgrade_armor = self.cost_dict.get('upgrade_armor')
        self.upgrade_ship = self.cost_dict.get('upgrade_ship')


@bp.route('/shop')
@login_required
def shop_get():
    cost = Cost()
    # TODO create class to store buttons states
    #buttons_state = {'heal_btn': True, 'upgrade_weapon_btn': False, 'upgrade_armor_btn': False, 'upgrade_ship_btn': True}
    return render_template('shop.html', heal_btn=True, upgrade_weapon_btn=False, upgrade_armor_btn=False, upgrade_ship_btn=True, cost=cost)


@bp.route('/shop/heal')
@login_required
def heal():
    print('Healing')
    return  redirect(url_for('bp_shop.shop_get'))


@bp.route('/shop/upgrade_weapon')
@login_required
def upgrade_weapon():
    print('Upgrade weapon')
    return redirect(url_for('bp_shop.shop_get'))


@bp.route('/shop/upgrade_armor')
@login_required
def upgrade_armor():
    print('Upgrade armor')
    return redirect(url_for('bp_shop.shop_get'))


@bp.route('/shop/upgrade_ship')
@login_required
def upgrade_ship():
    print('Upgrade ship')
    return redirect(url_for('bp_shop.shop_get'))