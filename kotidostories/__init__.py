from flask import Flask

def create_app():
    app = Flask(__name__)
    with app.app_context():
        from kotidostories.routes import landing_bp
        app.register_blueprint(landing_bp)
    return app

