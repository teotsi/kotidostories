from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # loading config.py
    app.config.from_object('kotidostories.config.Config')
    # initializing db
    db.init_app(app)

    with app.app_context():
        import kotidostories.models
        db.create_all()

        # registering blueprints
        from kotidostories.routes import landing_bp
        app.register_blueprint(landing_bp)
    return app
