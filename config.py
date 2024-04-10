class Config:
    DEBUG = True
    SECRET_KEY = 'your_secret_key'  # Change this to a random secret key
    SQLALCHEMY_DATABASE_URI = 'postgresql://stephen_oa:stephen1123@localhost/fpp_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'your_jwt_secret_key'  # Change this to a random JWT secret key


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    JWT_SECRET_KEY = 'test_secret_key'
