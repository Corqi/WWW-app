from .app import db
import datetime
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    character_type = db.Column(db.Integer, default=0)
    current_health = db.Column(db.Integer, default=100)
    max_health = db.Column(db.Integer, default=100)
    money = db.Column(db.Integer, default=10)
    speed = db.Column(db.Integer, default=1)
    armor = db.Column(db.Integer, default=1)
    luck = db.Column(db.Integer, default=1)
    chat_messages = db.relationship('Message', back_populates="user", lazy=True)
    mission_handler = db.relationship('MissionHandler', back_populates="user")
    is_free = db.Column(db.String(5), default="true")
    last_death_time = db.Column(db.DateTime)

    def __init__(self, email, password, name):
        self.email = email
        self.password = password
        self.name = name


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.datetime.now())
    user = db.relationship("User", back_populates="chat_messages", lazy=False)

    def __init__(self, user_id, content):
        self.user_id = user_id
        self.content = content


class Mission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    danger_level = db.Column(db.Integer)

    def __init__(self, title, content, danger_level):
        self.title = title
        self.content = content
        self.danger_level = danger_level


class MissionHandler(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    last_missions_update = db.Column(db.DateTime(), nullable=False, default=datetime.datetime.now())
    mission_taken_time = db.Column(db.DateTime())
    easy_mission_id = db.Column(db.Integer, default=1)
    medium_mission_id = db.Column(db.Integer, default=2)
    hard_mission_id = db.Column(db.Integer, default=3)
    mission_picked_id = db.Column(db.Integer, default=0)
    easy_mission_cost = db.Column(db.Integer, default=5)
    medium_mission_cost = db.Column(db.Integer, default=12)
    hard_mission_cost = db.Column(db.Integer, default=26)
    easy_mission_duration = db.Column(db.Integer, default=30)
    medium_mission_duration = db.Column(db.Integer, default=60)
    hard_mission_duration = db.Column(db.Integer, default=120)
    user = db.relationship("User", back_populates="mission_handler")
    mission_bg = db.Column(db.Integer, default=1)

    def __init__(self, user_id):
        self.user_id = user_id
