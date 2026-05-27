from app import db
from app.models.models import User, Post
from datetime import datetime

def validate_user_password(username, password):
    user = db.session.query(User).filter_by(username=username).first()
    if user and user.password == password:
        user.last_login = datetime.utcnow()
        db.session.commit()
        return user
    return None

def user_exists(username):
    return db.session.query(User).filter_by(username=username).first()

def create_user(username, password, avatar_url=None, bio=None):
    new_user = User(username=username, password=password, avatar_url=avatar_url, bio=bio)
    db.session.add(new_user)
    db.session.commit()
    return new_user

def create_post(body, author_user):
    new_post = Post(body=body, author=author_user)
    db.session.add(new_post)
    db.session.commit()
    return new_post

def get_timeline():
    return db.session.query(Post).order_by(Post.timestamp.desc()).limit(5).all()