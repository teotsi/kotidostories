from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    # loading config.py
    app.config.from_object('kotidostories.config.Config')
    # initializing db
    db.init_app(app)

    # configuring authentication manager
    login_manager.login_view = 'auth.log_in'
    login_manager.init_app(app)
    with app.app_context():
        import kotidostories.models
        db.create_all()

        @login_manager.user_loader
        def load_user(user_id):
            from kotidostories.models import User
            return User.query.get(user_id)

        # registering blueprints
        from kotidostories.routes import landing_bp, auth_bp, posting_bp
        app.register_blueprint(landing_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(posting_bp)
    return app
