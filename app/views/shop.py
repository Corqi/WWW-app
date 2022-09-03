from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from ..app import db

bp = Blueprint('bp_shop', __name__)


class Cost:
    # TODO Write logic to calculate costs according to levels
    cost_dict = {'heal': 10, 'upgrade_weapon': 100, 'upgrade_armor': 1000, 'upgrade_ship': 0}

    def __init__(self):
        self.heal = self.cost_dict.get('heal')
        self.heal_bonus = 10
        self.upgrade_weapon = self.cost_dict.get('upgrade_weapon')
        self.luck_bonus = 1
        self.upgrade_armor = self.cost_dict.get('upgrade_armor')
        self.armor_bonus = 1
        self.upgrade_ship = self.cost_dict.get('upgrade_ship')
        self.speed_bonus = 1

        self.services_cost = {'heal': self.heal, 'upgrade_weapon': self.upgrade_weapon,
                              'upgrade_armor': self.upgrade_armor, 'upgrade_ship': self.upgrade_ship}


class Buttons:
    def __init__(self):
        self.heal_btn = False
        self.upgrade_weapon_btn = False
        self.upgrade_armor_btn = False
        self.upgrade_ship_btn = False

        self.state = {'heal': self.heal_btn, 'upgrade_weapon': self.upgrade_weapon_btn,
                      'upgrade_armor': self.upgrade_armor_btn,
                      'upgrade_ship': self.upgrade_ship_btn}


@bp.route('/shop')
@login_required
def shop_get():
    cost = Cost()
    buttons = Buttons()

    # Setting buttons state
    for k in buttons.state.keys():
        if cost.services_cost.get(k) > current_user.money:
            buttons.state[k] = False
        else:
            buttons.state[k] = True

    if current_user.current_health >= current_user.max_health:
        buttons.state['heal'] = False

    return render_template('shop.html', state=buttons.state, cost=cost)


@bp.route('/shop/heal')
@login_required
def heal():
    cost = Cost()
    if current_user.current_health >= current_user.max_health:
        flash('You have enough health points')
        return redirect(url_for('bp_shop.shop_get'))

    if current_user.money >= cost.heal:
        current_user.money -= cost.heal
        current_user.current_health += cost.heal_bonus
        db.session.commit()
        flash('Heal message')
        return redirect(url_for('bp_shop.shop_get'))

    flash('No money message')
    return redirect(url_for('bp_shop.shop_get'))


@bp.route('/shop/upgrade_weapon')
@login_required
def upgrade_weapon():
    cost = Cost()

    if current_user.money >= cost.upgrade_weapon:
        current_user.money -= cost.upgrade_weapon
        current_user.luck += cost.luck_bonus
        db.session.commit()
        flash('Upgrade weapon message')
        return redirect(url_for('bp_shop.shop_get'))

    flash('No money message')
    return redirect(url_for('bp_shop.shop_get'))


@bp.route('/shop/upgrade_armor')
@login_required
def upgrade_armor():
    cost = Cost()
    if current_user.money >= cost.upgrade_armor:
        current_user.money -= cost.upgrade_armor
        current_user.armor += cost.armor_bonus
        db.session.commit()
        flash('Upgrade armor message')
        return redirect(url_for('bp_shop.shop_get'))

    flash('No money message')
    return redirect(url_for('bp_shop.shop_get'))


@bp.route('/shop/upgrade_ship')
@login_required
def upgrade_ship():
    cost = Cost()
    if current_user.money >= cost.upgrade_ship:
        current_user.money -= cost.upgrade_ship
        current_user.speed += cost.speed_bonus
        db.session.commit()
        flash('Upgrade ship message')
        return redirect(url_for('bp_shop.shop_get'))

    flash('No money message')
    return redirect(url_for('bp_shop.shop_get'))
