## 🚀 Flask 기반 Rest API Backend Server

## 0. 개요

학교 소식을 전달하고 받아보는 학교 소식 뉴스피드의 간단한 구현 예제입니다.
자세한 예외처리는 생략하였으니 이점 참고해주세요.


## 1. 환경

* Python 3.8
* Mysql 8.2.0

## 2. 가상 환경 세팅

```bash
pip3 install virtualenv
python3.8 -m virtualenv venv
source venv/bin/activate
```

## 3. 서버 구동 순서

```bash
pip install -r requirements.txt

# id, password, ip, db_name 자신의 환경에 맞게 설정해주세요.

# 환경 변수 설정 (Mac/Linux/Unix)
export DATABASE_URL='mysql+pymysql://<id>:<password>@<ip>/<db_name>'
# 환경 변수 설정 (Window)
set DATABASE_URL=mysql+pymysql://<id>:<password>@<ip>/<db_name>

# DB 생성 및 스키마 생성
python set_up_db.py

# 서버 구동
flask run
```

## 4. 테스트 코드 실행

```bash
# 테스트 코드 실행 시, 테스트 종료 후 데이터베이스의 스키마와 데이터가 모두 제거되므로 주의하세요.
pytest
```


## 5. 스키마 모델 변경 및 반영시 적용법

```bash
1. 모델 스키마 변경시 DB 에 반영 준비

flask db migrate -m "<관련 내용 메모 작성>"

2. DB 반영 적용

flask db upgrade
```

---

## 6. API Specification

### 1. Social Login
- **Endpoint**: `POST /api/social_login`
- **Description**: 사용자를 소셜 미디어 계정으로 인증하고 JWT 액세스 토큰을 발급합니다.
- **Request Body**:
  ```json
  {
    "social_type": "google",
    "social_id": "user123",
    "name": "Test User",
    "email": "test@example.com"
  }
  ```
- **Responses**:
  - **200 OK**:
    ```json
    {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
    ```

### 2. Update User Information
- **Endpoint**: `POST /api/users/update`
- **Description**: 현재 로그인한 사용자의 정보를 업데이트합니다.
- **Authorization**: Bearer Token (JWT 필요)
- **Request Body**:
  ```json
  {
    "role": "admin",
    "name": "Updated Name"
  }
  ```
- **Responses**:
  - **200 OK**:
    ```json
    {
      "id": 1,
      "role": "admin",
      "name": "Updated Name",
      "email": "test@example.com"
    }
    ```

### 3. Publish News
- **Endpoint**: `POST /api/publish_news`
- **Description**: 학교 관리자가 뉴스를 게시합니다.
- **Authorization**: Bearer Token (JWT 필요)
- **Request Body**:
  ```json
  {
    "school_id": 1,
    "title": "Important News",
    "content": "Important news content."
  }
  ```
- **Responses**:
  - **201 Created**:
    ```json
    {
      "id": 1,
      "title": "Important News",
      "content": "Important news content."
    }
    ```

### 4. Delete News
- **Endpoint**: `POST /api/delete_news`
- **Description**: 관리자가 뉴스를 삭제합니다.
- **Authorization**: Bearer Token (JWT 필요)
- **Request Body**:
  ```json
  {
    "news_id": 1
  }
  ```
- **Responses**:
  - **200 OK**:
    ```json
    {
      "msg": "News marked as deleted"
    }
    ```

### 5. My News Feed
- **Endpoint**: `POST /api/my_news_feed`
- **Description**: 사용자가 구독한 학교의 최신 뉴스를 조회합니다.
- **Authorization**: Bearer Token (JWT 필요)
- **Responses**:
  - **200 OK**:
    ```json
    [
      {
        "news_id": 1,
        "title": "Important News",
        "content": "Important news content.",
        "published_date": "2023-04-12T14:52:00Z",
        "school_id": 1
      }
    ]
    ```

### 6. Create School
- **Endpoint**: `POST /api/create/schools`
- **Description**: 관리자가 새로운 학교를 생성합니다.
- **Authorization**: Bearer Token (JWT 필요)
- **Request Body**:
  ```json
  {
    "name": "New School",
    "region": "New Region"
  }
  ```
- **Responses**:
  - **201 Created**:
    ```json
    {
      "id": 1,
      "name": "New School",
      "region": "New Region"
    }
    ```

### 7. Subscribe to School
- **Endpoint**: `POST /api/subscribe_school`
- **Description**: 사용자가 학교에 구독합니다.
- **Authorization**: Bearer Token (JWT 필요)
- **Request Body**:
  ```json
  {
    "school_id": 1
  }
  ```
- **Responses**:
  - **201 Created**:
    ```json
    {
      "msg": "Subscribed successfully"
    }
    ```

### 8. List Subscribed Schools
- **Endpoint**: `POST /api/subscribed_schools`
- **Description**: 사용자가 구독 중인 학교 목록을 조회합니다.
- **Authorization**: Bearer Token (JWT 필요)
- **Responses**:
  - **200 OK**:
    ```json
    [
      {
        "id": 1,
        "name": "New School",
        "region": "New Region"
      }
    ]
    ```

### 9. Unsubscribe from School
- **Endpoint**: `POST /api/unsubscribe_school`
- **Description**: 사용자가 학교 구독을 취소합니다.
- **Authorization**: Bearer Token (JWT 필요)
- **Request Body**:
  ```json
  {
    "school_id": 1
  }
  ```
- **Responses**:
  - **200 OK**:
    ```json
    {
      "msg": "Unsubscribed successfully"
    }
    ```

### 10. List News from Subscribed Schools
- **Endpoint**: `POST /api/subscribed_schools_news`
- **Description**: 사용자가 구독한 학교들에서 발행된 뉴스를 조회합니다.
- **Authorization**: Bearer Token (JWT 필요)
- **Responses**:
  - **200 OK**:
    ```json
    [
      {
        "news_id": 1,
        "title": "Important News",
        "content": "Important news content.",
        "published_date": "2023-04-12T14:52:00Z",
        "school_id": 1
      }
    ]
    ```
