import jwt
from elasticsearch import Elasticsearch
from flask import Flask, request
from flask_admin import Admin
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_mail import Mail
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from redis import Redis
from rq import Queue
import os
from .utils.general_utils import create_pictures_directory

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
login_manager = LoginManager()
secret = 'I know all about security'
mail = Mail()
r = Redis()
q = Queue(connection=r)
es = Elasticsearch(hosts=[{'host': os.environ.get(
    'ES_HOST', default='localhost'), 'port': 9200}])


def create_app(test_config=None, environment=None):
    app = Flask(__name__)
    if environment:
        app.config.from_object(
            f'kotidostories.config.{environment.capitalize()}Config')
    elif test_config:
        app.config.from_mapping(test_config)
    else:
        app.config.from_object('kotidostories.config.Config')
    # checking if pictures directory exists
    create_pictures_directory()
    # initializing db
    db.init_app(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['SESSION_COOKIE_HTTPONLY'] = False
    # configuring authentication manager
    login_manager.login_view = 'auth.log_in'
    login_manager.init_app(app)
    with app.app_context():
        import kotidostories.models
        db.create_all()
        mail.init_app(app)
        from .models import User, Post, Comment, Follower, Reaction
        from .admin.modelViews import AdminModelView, MyAdminIndexView
        admin = Admin(app, 'Example: Auth', index_view=MyAdminIndexView(
        ), base_template='my_master.html')
        admin.add_views(AdminModelView(User, db.session), AdminModelView(Post, db.session),
                        AdminModelView(Comment, db.session), AdminModelView(
                            Follower, db.session),
                        AdminModelView(Reaction, db.session))

        @login_manager.user_loader
        def load_user(user_id):
            from kotidostories.models import User
            return User.query.get(user_id)

        # registering blueprints
        from kotidostories.routes import landing_bp, auth_bp, posting_bp, commenting_bp, reacting_bp, images_bp, \
            discover_bp, direct_post_bp, direct_user_bp, suggest_bp, donating_bp
        app.register_blueprint(landing_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(posting_bp)
        app.register_blueprint(commenting_bp)
        app.register_blueprint(reacting_bp)
        app.register_blueprint(images_bp)
        app.register_blueprint(discover_bp)
        app.register_blueprint(direct_post_bp)
        app.register_blueprint(direct_user_bp)
        app.register_blueprint(suggest_bp)
        app.register_blueprint(donating_bp)

        @login_manager.request_loader
        def load_user_from_request(request):
            auth_headers = request.headers.get('Authorization', '').split()
            if len(auth_headers) != 2:
                return None
            try:
                token = auth_headers[1]
                data = jwt.decode(token, app.config['SECRET_KEY'])
                user = User.query.filter_by(email=data['sub']).first()
                if user:
                    return user
            except jwt.ExpiredSignatureError:
                return None
            except (jwt.InvalidTokenError, Exception) as e:
                return None
            return None

        @app.after_request
        def after_request(response):
            response.set_cookie('session', '', expires=0)
            if app.config['ENV'] == 'production':
                response.headers.add('Access-Control-Allow-Origin',
                                     'http://ec2-34-201-242-135.compute-1.amazonaws.com:3000/')
            else:
                response.headers.add(
                    'Access-Control-Allow-Origin', request.environ.get('HTTP_ORIGIN', 'localhost'))
            response.headers.add(
                'Access-Control-Allow-Headers', 'Content-Type,Authorization')
            response.headers.add(
                'Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,PATCH')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response
    return app
