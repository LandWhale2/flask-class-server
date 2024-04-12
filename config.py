import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default-jwt-secret-key')


class DevelopmentConfig(Config):
    DEBUG = True
    ## 실제 환경에서는 URL 변경필요, 편의상 통일
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

class TestingConfig(Config):
    TESTING = True
    ## 실제 환경에서는 URL 변경필요, 편의상 통일
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    ## 실제 환경에서는 URL 변경필요, 편의상 통일
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
