from flask import Flask
from werkzeug.debug import DebuggedApplication

def create_app():
    # Create and configure the app
    app = Flask(__name__,
                instance_relative_config=False
                )
    
    # Turn on debug mode
    app.debug = True
    app.wsgi_app = DebuggedApplication(app.wsgi_app)

    # Register blueprints (views)
    from .views.default import bp as bp_default
    app.register_blueprint(bp_default)

    from .views.game import bp as bp_game
    app.register_blueprint(bp_game)


    # for localhost only
    app.run()
