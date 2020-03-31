import json
import os

import pytest
from flask_login import current_user

from kotidostories import create_app
from kotidostories.models import User


@pytest.fixture
def app():
    # try:
    #     os.remove('kotidostories/.testdb.sqlite')
    # except OSError:
    #     pass
    app = create_app({'DEBUG': True,
                      'SECRET_KEY': 'test key',
                      'ENV': 'development',
                      'SQLALCHEMY_DATABASE_URI': 'sqlite:///.testdb.sqlite?check_same_thread=False',
                      'SQLALCHEMY_TRACK_MODIFICATIONS': False})

    yield app


class Flag():
    flag = True


@pytest.fixture
def client(app):
    with app.app_context():
        if Flag.flag:
            from kotidostories import db, bcrypt
            db.session.add(User(username='testidis2', email='testy2@testy.testy',
                                password_hash=bcrypt.generate_password_hash('pass').decode('utf-8')))
            db.session.commit()
            Flag.flag = False
        with app.test_client() as client:
            yield client


def test_up(client):
    rv = client.get('/')
    assert 'OK' in rv.status


def test_check_username(client):
    rv = client.get('/checkUsername/testidis2') #testidis2 already exists!
    assert '401' in rv.status
    rv = client.get('/checkUsername/testidis') #testidis is available
    assert '200' in rv.status


def test_register(client):
    rv = client.post('/register', json={"email": "testy@testy.testy",
                                        "username": "testidis",
                                        "password": "pass",
                                        "remember_me": "True"
                                        })
    assert 'OK' in rv.status


def test_log_in(app, client):
    @app.login_manager.request_loader
    def load_user_from_request(request):
        return User.query.first()

    rv = client.post('/login/', json={"email": "testy@testy.testy",
                                      "password": "pass",
                                      "remember_me": "True"
                                      })
    assert 'OK' in rv.status


def test_upload_post(app, client):
    @app.login_manager.request_loader
    def load_user_from_request(request):
        return User.query.filter_by(username='testidis').first()

    rv = client.post('user/testidis/posts/', json={"content": "new post!",
                                                   "title": "WHOAAAA1",
                                                   "preview": "new preview!",
                                                   "category": "love"
                                                   })
    assert 'OK' in rv.status


def test_update_post(app, client):
    @app.login_manager.request_loader
    def load_user_from_request(request):
        return User.query.filter_by(username='testidis').first()

    initial_user = get_user(client)
    post = initial_user['posts'][0]
    rv = client.patch(f'user/testidis/posts/{post["id"]}', json={"content": "just a funny edit!"})
    assert 'OK' in rv.status
    user = get_user(client)
    edit_post = user['posts'][0]
    assert post != edit_post


def test_log_out(app, client):
    @app.login_manager.request_loader
    def load_user_from_request(request):
        return User.query.first()

    rv = client.get('/logout/')
    assert 'OK' in rv.status


def test_follow(app, client):
    @app.login_manager.request_loader
    def load_user_from_request(request):
        return User.query.filter_by(username='testidis').first()

    client.get('/logout/')
    rv = client.get('user/testidis2/follow')
    assert 'OK' in rv.status  # asserting successful follow
    user = get_user(client)
    assert user['following']
    rv = client.delete('user/testidis2/follow')
    user = get_user(client)
    assert not user['following']  # asserting unfollow


def test_comment(app, client):
    @app.login_manager.request_loader
    def load_user_from_request(request):
        return User.query.filter_by(username='testidis').first()

    post_id = current_user.posts[0].id
    rv = client.get(f'/user/{current_user.username}/posts/{post_id}/comments/')
    assert 'OK' in rv.status  # asserting successful follow
    comments = json.loads(rv.data)['comments']
    assert len(comments) == 0
    rv = client.post(f'/user/{current_user.username}/posts/{post_id}/comments/',
                     json={"content": "That story is great!"})
    assert 'OK' in rv.status
    rv = client.get(f'/user/{current_user.username}/posts/{current_user.posts[0].id}/comments/')
    comments = json.loads(rv.data)['comments']
    assert len(comments) == 1


@pytest.fixture(scope="session", autouse=True)
def cleanup(request):
    """Cleanup a testing directory once we are finished."""

    def remove_test_dir():
        try:
            os.remove('kotidostories/.testdb.sqlite')
        except OSError:
            pass

    request.addfinalizer(remove_test_dir)


def get_user(client):
    post_req = client.get('user/testidis/')
    assert 'OK' in post_req.status
    return json.loads(post_req.data)['user']


def log_in(client):
    rv = client.post('/login/', json={"email": "testy@testy.testy",
                                      "password": "pass",
                                      "remember_me": "True"
                                      })
    return rv
