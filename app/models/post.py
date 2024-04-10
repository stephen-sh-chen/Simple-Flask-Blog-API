from app import db
from datetime import datetime

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Post {self.title}>'

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "pub_date": self.pub_date.isoformat(),
            "author_id": self.author_id
        }
