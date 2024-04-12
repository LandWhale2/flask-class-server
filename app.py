from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from models import db
from routes.auth_routes import auth_bp
from routes.news_routes import news_bp
from routes.subscription_routes import subscribe_bp
from config import DevelopmentConfig



def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(news_bp)
    app.register_blueprint(subscribe_bp)

    @app.route('/')
    def ping():
        return "success"

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=4000, debug=True)

