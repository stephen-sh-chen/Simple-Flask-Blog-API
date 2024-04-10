from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_migrate import Migrate
from config import Config

# Create uninitialized extensions
db = SQLAlchemy()
jwt = JWTManager()
api = Api()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with the app instance
    db.init_app(app)
    jwt.init_app(app)

    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

    # Import and register resources
    from .resources.user import UserRegister, UserLogin, Helloworld
    from .resources.post import PostList, PostDetail
    api.add_resource(Helloworld, '/')
    api.add_resource(UserRegister, '/register')
    api.add_resource(UserLogin, '/login')
    api.add_resource(PostList, '/posts')
    api.add_resource(PostDetail, '/posts/<int:post_id>')
    api.init_app(app)

    return app
