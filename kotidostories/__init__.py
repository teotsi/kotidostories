from flask import Flask

def create_app():
    app = Flask(__name__)
    with app.app_context():
        app.config.from_object('kotidostories.config.Config')
        from kotidostories.routes import landing_bp
        app.register_blueprint(landing_bp)
    return app

