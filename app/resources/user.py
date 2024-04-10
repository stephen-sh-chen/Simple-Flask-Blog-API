from flask_restful import Resource, reqparse
from ..models.user import User
from app import db
from flask_jwt_extended import create_access_token, create_refresh_token

# Set up parser for user data
user_parser = reqparse.RequestParser()
user_parser.add_argument('username', help='This field cannot be blank', required=True)
user_parser.add_argument('password', help='This field cannot be blank', required=True)
user_parser.add_argument('email', help='This field cannot be blank', required=True)


class Helloworld(Resource):
    def get(self):
        return {'message':'hello world!'}


class UserRegister(Resource):
    def post(self):
        data = user_parser.parse_args()

        # Check if the user already exists
        if User.query.filter_by(username=data['username']).first():
            return {"message": "A user with that username already exists"}, 400

        user = User(
            username=data['username'],
            email=data['email']
        )
        user.set_password(data['password'])

        db.session.add(user)
        db.session.commit()

        return {"message": "User {} was created".format(data['username'])}, 201


class UserLogin(Resource):
    def post(self):
        data = user_parser.parse_args()
        user = User.query.filter_by(username=data['username']).first()

        if user and user.check_password(data['password']):
            # Create JWT tokens
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        else:
            return {'message': 'Invalid credentials'}, 401
