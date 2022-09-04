from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from ..app import db

from ..decorators import selected_character_required, is_free_true_required, is_alive_required

bp = Blueprint('bp_shop', __name__)


class Cost:
    cost_dict = {'heal': 30, 'upgrade_weapon': 15, 'upgrade_armor': 15, 'upgrade_ship': 15}

    def __init__(self, user):
        self.heal = self.cost_dict.get('heal')
        self.upgrade_weapon = self.cost_dict.get('upgrade_weapon') * user.luck
        self.luck_bonus = 1
        self.upgrade_armor = self.cost_dict.get('upgrade_armor') * user.armor
        self.armor_bonus = 1
        self.upgrade_ship = self.cost_dict.get('upgrade_ship') * user.speed
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
@selected_character_required
@is_free_true_required
@is_alive_required
def shop_get():

    cost = Cost(current_user)
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
@selected_character_required
@is_free_true_required
@is_alive_required
def heal():

    cost = Cost(current_user)
    if current_user.current_health >= current_user.max_health:
        flash('You have enough health points')
        return redirect(url_for('bp_shop.shop_get'))

    if current_user.money >= cost.heal:
        current_user.money -= cost.heal
        current_user.current_health = 100
        db.session.commit()
        flash('You should feel better now.')
        return redirect(url_for('bp_shop.shop_get'))

    flash('No money message')
    return redirect(url_for('bp_shop.shop_get'))


@bp.route('/shop/upgrade_weapon')
@login_required
@selected_character_required
@is_free_true_required
@is_alive_required
def upgrade_weapon():

    cost = Cost(current_user)

    if current_user.money >= cost.upgrade_weapon:
        current_user.money -= cost.upgrade_weapon
        current_user.luck += cost.luck_bonus
        db.session.commit()
        flash('I upgraded your gun a bit.')
        return redirect(url_for('bp_shop.shop_get'))

    flash('No money message')
    return redirect(url_for('bp_shop.shop_get'))


@bp.route('/shop/upgrade_armor')
@login_required
@selected_character_required
@is_free_true_required
@is_alive_required
def upgrade_armor():

    cost = Cost(current_user)
    if current_user.money >= cost.upgrade_armor:
        current_user.money -= cost.upgrade_armor
        current_user.armor += cost.armor_bonus
        db.session.commit()
        flash('I upgraded your armor a bit.')
        return redirect(url_for('bp_shop.shop_get'))

    flash('No money message')
    return redirect(url_for('bp_shop.shop_get'))


@bp.route('/shop/upgrade_ship')
@login_required
@selected_character_required
@is_free_true_required
@is_alive_required
def upgrade_ship():

    cost = Cost(current_user)
    if current_user.money >= cost.upgrade_ship:
        current_user.money -= cost.upgrade_ship
        current_user.speed += cost.speed_bonus
        db.session.commit()
        flash('I upgraded your spaceship a bit.')
        return redirect(url_for('bp_shop.shop_get'))

    flash('No money message')
    return redirect(url_for('bp_shop.shop_get'))
