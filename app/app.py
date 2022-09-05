from flask import Flask, flash, redirect, url_for, session
from werkzeug.debug import DebuggedApplication
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()

def create_app():
    # Create and configure the app
    app = Flask(__name__,
                instance_relative_config=False
                )

    # Load config from file config.py
    app.config.from_pyfile('config.py')

    # Turn on debug mode
    app.debug = True
    app.wsgi_app = DebuggedApplication(app.wsgi_app)

    # Setup database connection using standard pattern mysql://user:password@host/dbname
    app.config['SQLALCHEMY_DATABASE_URI'] = (f"mysql://{app.config['DB_USER']}:{app.config['DB_PASSWORD']}"
                                             f"@{app.config['DB_HOST']}/{app.config['DB_NAME']}")
    db.init_app(app)
    mail.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'bp_auth.login_get'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized():
        session.pop('_flashes', None)
        flash('Please log in to access this page!')
        print(login_manager.blueprint_login_views)
        return redirect(url_for('bp_auth.login_get'))

    with app.app_context():
        db.create_all()
        db.session.commit()

    # Register blueprints (views)
    from .views.auth import bp as bp_auth
    app.register_blueprint(bp_auth)

    from .views.game import bp as bp_game
    app.register_blueprint(bp_game)

    from .views.chat import bp as bp_chat
    app.register_blueprint(bp_chat)

    from .views.shop import bp as bp_shop
    app.register_blueprint(bp_shop)

    from .views.settings import bp as bp_settings
    app.register_blueprint(bp_settings)

    from .views.bar import bp as bp_bar
    app.register_blueprint(bp_bar)

    from .views.mission import bp as bp_mission
    app.register_blueprint(bp_mission)

    from .views.death import bp as bp_death
    app.register_blueprint(bp_death)

    from .views.choose import bp as bp_choose
    app.register_blueprint(bp_choose)

    # Register errors
    from .views.errors import page_not_found
    app.register_error_handler(404, page_not_found)

    # for localhost only
    app.run()
