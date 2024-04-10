from flask_restful import Resource, reqparse
from ..models.post import Post
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db

# Parser for creating and updating posts
post_parser = reqparse.RequestParser()
post_parser.add_argument('title', type=str, required=True, help='Title cannot be blank.')
post_parser.add_argument('body', type=str, required=True, help='Body cannot be blank.')


class PostList(Resource):
    def get(self):
        # Query all posts
        posts = Post.query.all()
        return [post.to_json() for post in posts], 200

    @jwt_required()
    def post(self):
        data = post_parser.parse_args()
        user_id = get_jwt_identity()  # Assuming the identity is user_id
        new_post = Post(title=data['title'], body=data['body'], author_id=user_id)

        db.session.add(new_post)
        db.session.commit()

        return new_post.to_json(), 201


class PostDetail(Resource):
    @jwt_required()
    def get(self, post_id):
        post = Post.query.get_or_404(post_id)
        return post.to_json(), 200

    @jwt_required()
    def put(self, post_id):
        data = post_parser.parse_args()
        post = Post.query.get_or_404(post_id)
        user_id = get_jwt_identity()  # Verify the user owns the post

        if post.author_id != user_id:
            return {"message": "You do not have permission to edit this post."}, 403

        post.title = data['title']
        post.body = data['body']
        db.session.commit()

        return post.to_json(), 200

    @jwt_required()
    def delete(self, post_id):
        post = Post.query.get_or_404(post_id)
        user_id = get_jwt_identity()  # Verify the user owns the post

        if post.author_id != user_id:
            return {"message": "You do not have permission to delete this post."}, 403

        db.session.delete(post)
        db.session.commit()

        return {"message": "Post deleted."}, 200
