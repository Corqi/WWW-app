from flask import Flask
from werkzeug.debug import DebuggedApplication
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

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


    from .models import User


    with app.app_context():
        db.create_all()
        db.session.commit()
        # admin = User('adminsds', 'admssin@edxample.com')
        # db.session.add(admin)
        # db.session.commit()
        users = User.query.all()
        print(users)


    # Register blueprints (views)
    from .views.auth import bp as bp_auth
    app.register_blueprint(bp_auth)

    from .views.game import bp as bp_game
    app.register_blueprint(bp_game)


    # for localhost only
    app.run()

