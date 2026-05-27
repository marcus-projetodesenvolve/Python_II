from datetime import datetime
from app import db, login
from flask_login import UserMixin
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import ForeignKey

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    avatar_url = db.Column(db.String(256), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    posts: Mapped[list['Post']] = relationship(back_populates='author', cascade='all, delete-orphan')

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    author: Mapped['User'] = relationship(back_populates='posts')

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))