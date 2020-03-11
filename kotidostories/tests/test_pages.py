import os
import tempfile

import flask
import pytest

from kotidostories import create_app


@pytest.fixture
def client():
    app = create_app({'DEBUG': True,
                      'SECRET_KEY': 'test key',
                      'ENV': 'development',
                      'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
                      'SQLALCHEMY_TRACK_MODIFICATIONS': False})

    with app.test_client() as client:
        yield client


def test_up(client):
    rv = client.get('/')
    assert 'OK' in rv.status

#
# def test_register(client):
#     rv = client.post('/register', json={"email": "test@test.gs",
#                                         "username": "teosss",
#                                         "password": "pass",
#                                         "remember_me": "True"
#                                         })
#     assert 'OK' in rv.status
#
#
# def test_log_out(client):
#     rv = client.get('/logout')
#     assert 'OK' in rv.status


def test_log_in(client):
    rv = client.post('/login', json={"email": "test@test.gs",
                                     "password": "pass",
                                     "remember_me": "True"
                                     })
    assert 'OK' in rv.status
