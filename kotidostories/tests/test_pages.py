import os
import tempfile

import flask
import pytest

from kotidostories import create_app


@pytest.fixture
def client():
    app = create_app()
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


def test_up(client):
    rv = client.get('/')
    assert 'OK' in rv.status

#
# def test_register(client):
#     rv = client.post('/register', json={"email": "tes55t@test.gs",
#                                         "username":"teosss",
#                                         "password": "pass",
#                                         "remember_me": "True"
#                                         })
#     assert 'OK' in rv.status


def test_log_in(client):
    rv = client.post('/login', json={"email": "test@test.gs",
                                     "password": "pass",
                                     "remember_me": "True"
                                     })
    assert 'OK' in rv.status
