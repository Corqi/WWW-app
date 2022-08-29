from .app import db
import datetime
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    level = db.Column(db.Integer, default=0)
    currentHealth = db.Column(db.Integer, default=100)
    maxHealth = db.Column(db.Integer, default=100)
    money = db.Column(db.Integer, default=10)
    speed = db.Column(db.Integer, default=1)
    armor = db.Column(db.Integer, default=1)
    luck = db.Column(db.Integer, default=1)
    chat_messages = db.relationship('Message', back_populates="user", lazy=True)

    def __init__(self, email, password, name):
        self.email = email
        self.password = password
        self.name = name


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.datetime.utcnow)
    user = db.relationship("User", back_populates="chat_messages", lazy=False)

    def __init__(self, user_id, content):
        self.user_id = user_id
        self.content = content