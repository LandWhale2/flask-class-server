import pytest
from flask import json
from app import create_app
from models import db, User, School, Subscription, News
from flask_jwt_extended import create_access_token

@pytest.fixture
def client():
    app = create_app(config_class='config.TestingConfig')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            admin = User(name="Admin", email="admin@example.com", role="admin")
            user = User(name="User", email="user@example.com", role="user")
            db.session.add(admin)
            db.session.add(user)
            db.session.commit()
            school = School(name="Test School", region="Test Region", admin_id=admin.id)
            db.session.add(school)
            db.session.commit()
        yield client
        with app.app_context():
            db.drop_all()

@pytest.fixture
def admin_token(client):
    with client.application.app_context():
        admin = User.query.filter_by(email="admin@example.com").first()
        return create_access_token(identity=admin.id)

@pytest.fixture
def user_token(client):
    with client.application.app_context():
        user = User.query.filter_by(email="user@example.com").first()
        return create_access_token(identity=user.id)

def test_create_school(client, admin_token):
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = client.post('/api/create/schools', headers=headers, json={
        'name': 'New School',
        'region': 'New Region'
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['name'] == 'New School'

def test_subscribe_school(client, user_token):
    headers = {'Authorization': f'Bearer {user_token}'}
    response = client.post('/api/subscribe_school', headers=headers, json={'school_id': 1})
    assert response.status_code == 201
    assert 'Subscribed successfully' in json.loads(response.data)['msg']

def test_unsubscribe_school(client, user_token):
    headers = {'Authorization': f'Bearer {user_token}'}
    client.post('/api/subscribe_school', headers=headers, json={'school_id': 1})  # 먼저 구독
    response = client.post('/api/unsubscribe_school', headers=headers, json={'school_id': 1})
    assert response.status_code == 200
    assert 'Unsubscribed successfully' in json.loads(response.data)['msg']

def test_subscribed_schools(client, user_token):
    headers = {'Authorization': f'Bearer {user_token}'}
    client.post('/api/subscribe_school', headers=headers, json={'school_id': 1})
    response = client.post('/api/subscribed_schools', headers=headers)
    assert response.status_code == 200
    schools = json.loads(response.data)
    assert len(schools) == 1
    assert schools[0]['name'] == 'Test School'

def test_subscribed_schools_news(client, user_token):
    headers = {'Authorization': f'Bearer {user_token}'}
    client.post('/api/subscribe_school', headers=headers, json={'school_id': 1})
    response = client.post('/api/subscribed_schools_news', headers=headers)
    assert response.status_code == 200
    news_list = json.loads(response.data)
    assert len(news_list) == 0
