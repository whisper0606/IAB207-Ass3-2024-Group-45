from . import db
from datetime import datetime
from flask_login import UserMixin
from enum import Enum

class User(db.Model): # TODO - ADD UserMixin WHEN WORKING ON AUTHENTICAITON
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    comments = db.relationship('Comment', backref='user')
    orders = db.relationship('Order', backref='user')
    
    def __repr__(self):
        return f"Name: {self.name}"

class Event(db.Model):
    __tablename__ = 'events'

    class Genre(Enum):
        ROCK_ALT = "Rock/Alternative"
        POP = "Pop"
        EDM = "Electronic/Dance"
        HIPHOP_RNB = "Hip-Hop/R&B"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    description = db.Column(db.String(512), index=True, nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    venue = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.Enum(Genre), nullable=False)
    image = db.Column(db.String(400))
    creator_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    comments = db.relationship('Comment', backref='event')
    orders = db.relationship('Order', backref='event')

    def __repr__(self):
        return f"Event: {self.name}"

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)

    def __repr__(self):
        return f"Comment: {self.text}"
    

class Order(db.Model):
    __tablename__ = 'orders'
    class Type(Enum):
        NORMAL = "General Admission"
        VIP = "VIP"
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Enum(Type), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)

    def __repr__(self):
        return f"Order: {self.id}"





