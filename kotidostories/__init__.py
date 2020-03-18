from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
login_manager = LoginManager()
secret = 'I know all about security'
mail = Mail()


def create_app(test_config=None):
    app = Flask(__name__)
    if test_config:
        app.config.from_mapping(test_config)
    else:
        # loading config.py
        app.config.from_object('kotidostories.config.Config')
    # initializing db
    db.init_app(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    # configuring authentication manager
    login_manager.login_view = 'auth.log_in'
    login_manager.init_app(app)
    with app.app_context():
        import kotidostories.models
        db.create_all()
        mail.init_app(app)
        @login_manager.user_loader
        def load_user(user_id):
            from kotidostories.models import User
            return User.query.get(user_id)

        # registering blueprints
        from kotidostories.routes import landing_bp, auth_bp, posting_bp, commenting_bp
        app.register_blueprint(landing_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(posting_bp)
        app.register_blueprint(commenting_bp)

        @app.after_request
        def after_request(response):
            response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response
    return app
