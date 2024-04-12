import pytest

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import json
from app import create_app
from models import db, User
from flask_jwt_extended import create_access_token

@pytest.fixture
def client():
    app = create_app(config_class='config.TestingConfig')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()

            user = User(
                name="Existing User",
                email="existing@example.com",
                social_type="google",
                social_id="existing123"
            )
            db.session.add(user)
            db.session.commit()
        yield client
        with app.app_context():
            db.drop_all()

def test_social_login_existing_user(client):
    response = client.post('/api/social_login', json={
        'social_type': 'google',
        'social_id': 'existing123',
        'name': 'Existing User',
        'email': 'existing@example.com'
    })
    data = json.loads(response.data)
    assert response.status_code == 200
    assert 'access_token' in data

def test_social_login_new_user(client):
    response = client.post('/api/social_login', json={
        'social_type': 'facebook',
        'social_id': 'new12345',
        'name': 'New User',
        'email': 'new@example.com'
    })
    data = json.loads(response.data)
    assert response.status_code == 200
    assert 'access_token' in data

def test_update_user_info(client):
    with client.application.app_context():
        user = User.query.first()
        access_token = create_access_token(identity=user.id)
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = client.post('/api/users/update', headers=headers, json={
        'name': 'Updated Name',
        'role': 'admin'
    })
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['name'] == 'Updated Name'
    assert data['role'] == 'admin'
    assert data['email'] == user.email

