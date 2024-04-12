import pytest
from flask import json
from app import create_app
from models import db, News, School, User, Subscription, UserNewsFeed
from flask_jwt_extended import create_access_token

@pytest.fixture
def client():
    app = create_app(config_class='config.TestingConfig')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # 사용자와 관리자 생성 및 커밋
            user = User(name="Test User", email="testuser@example.com")
            admin = User(name="Admin User", email="adminuser@example.com")
            db.session.add(user)
            db.session.add(admin)
            db.session.commit()  # 모든 변경사항 커밋

            # admin_id가 커밋된 후에 School 객체 생성
            school = School(name="Test School", region="Test Region", admin_id=admin.id)
            db.session.add(school)
            db.session.commit()

        yield client
        with app.app_context():
            db.drop_all()

@pytest.fixture
def tokens(client):
    with client.application.app_context():
        normal_user = User.query.filter_by(email="testuser@example.com").first()
        admin_user = User.query.filter_by(email="adminuser@example.com").first()
        user_token = create_access_token(identity=normal_user.id)
        admin_token = create_access_token(identity=admin_user.id)
    return user_token, admin_token

def test_publish_news(client, tokens):
    user_token, admin_token = tokens
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = client.post('/api/publish_news', headers=headers, json={
        'school_id': 1,
        'title': 'New Event',
        'content': 'Details about the event.'
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['title'] == 'New Event'

def test_unauthorized_publish_news(client, tokens):
    user_token, admin_token = tokens
    headers = {'Authorization': f'Bearer {user_token}'}
    response = client.post('/api/publish_news', headers=headers, json={
        'school_id': 1,
        'title': 'Failed Event',
        'content': 'Should not be published.'
    })
    assert response.status_code == 403

def test_delete_news(client, tokens):
    user_token, admin_token = tokens
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = client.post('/api/publish_news', headers=headers, json={
        'school_id': 1,
        'title': 'Old News',
        'content': 'Old news content.'
    })
    news_id = json.loads(response.data)['id']
    del_response = client.post('/api/delete_news', headers=headers, json={'news_id': news_id})
    assert del_response.status_code == 200
    assert 'News marked as deleted' in del_response.json['msg']

def test_my_news_feed(client, tokens):
    user_token, admin_token = tokens
    headers = {'Authorization': f'Bearer {user_token}'}
    response = client.post('/api/my_news_feed', headers=headers)
    assert response.status_code == 200
    news_list = json.loads(response.data)
    assert isinstance(news_list, list)
