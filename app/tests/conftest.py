import pytest
from app import create_app, db
from config import TestConfig


@pytest.fixture(scope='session')
def test_app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app  # This provides the app to your tests
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='module')
def test_client(test_app):
    return test_app.test_client()


@pytest.fixture(scope='module')
def signup_default_user(test_client):
    response = test_client.post('/register', json={
        'username': 'default_user',
        'password': 'default_password',
        'email': 'default_user@example.com'
    })


@pytest.fixture(scope='module')
def auth_token(test_client, signup_default_user):
    login_response = test_client.post('/login', json={
        'username': 'default_user',
        'password': 'default_password',
        'email': 'default_user@example.com'
    })
    assert login_response.status_code == 200
    data = login_response.get_json()
    return data['access_token']

@pytest.fixture(scope='module')
def create_default_posts(test_client, auth_token):
    for i in range(1, 4):
        response = test_client.post('/posts', json={
            'title': f'New Blog Post {i}',
            'body': f'This is new blog post number {i}.'
        }, headers={'Authorization': f'Bearer {auth_token}'})
        assert response.status_code == 201