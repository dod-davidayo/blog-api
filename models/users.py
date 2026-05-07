from app import db
from models.post import Post

class User(db.Model):
    # explicit table name
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(225), nullable=False)
    user_role = db.Column(db.String(20), nullable=False, default='user')

    # one user to many relationship with posts
    posts = db.relationship('Post', backref='author', lazy=True)