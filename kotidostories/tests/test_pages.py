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
    """Start with a blank database."""
    rv = client.get('/')
    assert 'OK' in rv.status

