import json
import os

import pytest
from flask_login import current_user

from kotidostories import create_app
from kotidostories.models import User
from kotidostories.utils.es_utils import delete_post_from_index


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
    rv = client.get('/checkUsername/testidis2')  # testidis2 already exists!
    assert '401' in rv.status
    rv = client.get('/checkUsername/testidis')  # testidis is available
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

    post_id = get_user(client)['posts'][0]['id']

    rv = client.get(f'/user/{current_user.username}/posts/{post_id}/comments/')
    assert 'OK' in rv.status  # asserting successful comment GET
    comments = json.loads(rv.data)['comments']
    assert len(comments) == 0
    content = "That story is great!"
    rv = client.post(f'/user/{current_user.username}/posts/{post_id}/comments/',
                     json={"content": content})
    assert 'OK' in rv.status

    rv = client.get(f'/user/{current_user.username}/posts/{post_id}/comments/')
    comments = json.loads(rv.data)['comments']
    assert len(comments) == 1  # asserting that the comment was actually posted
    assert comments[0]['content'] == content  # asserting that the content is posted correctly

    comment_id = comments[0]['id']
    rv = client.patch(f'/user/{current_user.username}/posts/{post_id}/comments/{comment_id}/',
                      json={"content": "On a second note, I don't like this story. At all."})
    assert 'OK' in rv.status

    rv = client.get(f'/user/{current_user.username}/posts/{post_id}/comments/')
    comments = json.loads(rv.data)['comments']
    assert comments[0]['content'] != content  # asserting that the change was successful

    rv = client.delete(f'/user/{current_user.username}/posts/{post_id}/comments/{comment_id}/')
    assert 'OK' in rv.status
    rv = client.get(f'/user/{current_user.username}/posts/{post_id}/comments/')
    comments = json.loads(rv.data)['comments']
    assert len(comments) == 0


def test_reaction(app, client):
    @app.login_manager.request_loader
    def load_user_from_request(request):
        return User.query.filter_by(username='testidis').first()

    user = get_user(client)
    post_id = user['posts'][0]['id']
    username = user['username']

    rv = client.get(f'/user/{username}/posts/{post_id}/reaction/')
    assert 'OK' in rv.status  # asserting successful reaction GET
    reactions = json.loads(rv.data)['reactions']
    assert len(reactions) == 0
    assert 'OK' in rv.status

    rv = client.post(f'/user/{username}/posts/{post_id}/reaction/', json={'type': 'love'})
    assert 'OK' in rv.status  # asserting successful reaction POST
    rv = client.get(f'/user/{current_user.username}/posts/{post_id}/reaction/')
    reactions = json.loads(rv.data)['reactions']
    initial_type = 'love'
    assert reactions[0]['type'] == initial_type

    reaction_id = reactions[0]['id']

    rv = client.put(f'/user/{username}/posts/{post_id}/reaction/{reaction_id}', json={'type': 'inspiring'})
    assert 'OK' in rv.status
    rv = client.get(f'/user/{current_user.username}/posts/{post_id}/reaction/{reaction_id}')
    assert 'OK' in rv.status
    reaction_type = json.loads(rv.data)['reaction']['type']
    assert reaction_type != initial_type

    # delete posts from es
    rv = client.get('user/testidis/posts/')
    posts = json.loads(rv.data)['posts']
    for post in posts:
        delete_post_from_index(post["id"])


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
