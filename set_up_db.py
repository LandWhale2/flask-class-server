from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import os

# Flask 애플리케이션 및 설정
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 데이터베이스 엔진 및 SQLAlchemy 설정
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
db = SQLAlchemy(app)
migrate = Migrate(app, db)

def set_up_database():
    # 데이터베이스 존재 여부 확인 및 생성
    if not database_exists(engine.url):
        create_database(engine.url)
        print("Database created.")
    else:
        print("Database already exists.")

    # Flask 애플리케이션 컨텍스트 내에서 Flask-Migrate 업그레이드 실행
    with app.app_context():
        upgrade()
        print("Database upgraded to the latest version.")

if __name__ == '__main__':
    set_up_database()
