import pytest
from flask import json
from app import create_app
from models import db, User, School, News, Subscription, UserNewsFeed
from flask_jwt_extended import create_access_token

@pytest.fixture
def client():
    app = create_app(config_class='config.TestingConfig')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_full_user_workflow(client):

    # 소셜 로그인으로 새 사용자 생성
    response = client.post('/api/social_login', json={
        'social_type': 'google',
        'social_id': 'user123',
        'name': 'Test User',
        'email': 'test@example.com'
    })
    assert response.status_code == 200
    user_data = json.loads(response.data)

    user_token = user_data['access_token']

    # 새로운 사용자로 학교 생성 시도 (실패 예상)
    response = client.post('/api/create/schools', headers={'Authorization': f'Bearer {user_token}'}, json={
        'name': 'New School',
        'region': 'Test Region'
    })
    assert response.status_code == 403

    # 사용자 권한을 'admin'으로 업데이트
    response = client.post('/api/users/update', headers={'Authorization': f'Bearer {user_token}'}, json={
        'role': 'admin'
    })
    assert response.status_code == 200

    # 업데이트된 권한으로 학교 생성
    response = client.post('/api/create/schools', headers={'Authorization': f'Bearer {user_token}'}, json={
        'name': 'Authorized School',
        'region': 'Authorized Region'
    })
    assert response.status_code == 201
    school_id = json.loads(response.data)['id']

    # 관리자로 뉴스 게시
    response = client.post('/api/publish_news', headers={'Authorization': f'Bearer {user_token}'}, json={
        'school_id': school_id,
        'title': 'Important News',
        'content': 'Important news content.'
    })
    assert response.status_code == 201
    news_id = json.loads(response.data)['id']

    # 학교 구독
    response = client.post('/api/subscribe_school', headers={'Authorization': f'Bearer {user_token}'}, json={'school_id': school_id})
    assert response.status_code == 201

    # 구독한 학교의 뉴스 피드 확인
    response = client.post('/api/subscribed_schools_news', headers={'Authorization': f'Bearer {user_token}'})
    assert response.status_code == 200
    news_list = json.loads(response.data)
    assert any(news['news_id'] == news_id for news in news_list)

    # 구독 취소
    response = client.post('/api/unsubscribe_school', headers={'Authorization': f'Bearer {user_token}'}, json={'school_id': school_id})
    assert response.status_code == 200
