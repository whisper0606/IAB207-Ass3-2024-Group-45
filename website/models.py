from . import db
from datetime import datetime
from flask_login import UserMixin
from enum import Enum

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    events = db.relationship('Event', backref='creator', lazy=True)  # "creator" backref on Event
    comments = db.relationship('Comment', backref='author', lazy=True)  # "author" backref on Comment
    orders = db.relationship('Order', backref='buyer', lazy=True)  # "buyer" backref on Order
    
    def __repr__(self):
        return f"Name: {self.first_name} {self.last_name}, Email: {self.email}"

class Event(db.Model):
    __tablename__ = 'events'

    class Genre(Enum):
        ROCK_ALT = "Rock/Alternative"
        POP_FOLK = "Pop/Folk"
        EDM = "Electronic/Dance"
        HIPHOP_RNB = "Hip-Hop/R&B"

        def __str__(self):
            return self.value

    class Status(Enum):
        OPEN = "Open"
        SOLDOUT = "Sold Out"
        CANCELLED = "Cancelled"
        INACTIVE = "Inactive"

        def __str__(self):
            return self.value

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    venue = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.Enum(Genre), nullable=False)
    ticket_price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(400))
    status = db.Column(db.Enum(Status), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    comments = db.relationship('Comment', backref='event', lazy=True)  # "event" backref on Comment
    orders = db.relationship('Order', backref='event', lazy=True)  # "event" backref on Order

    def __repr__(self):
        return f"Event\nName: {self.name}\nDateTime: {self.datetime}\nVenue: {self.venue}\nGenre: {self.genre}\nTicket Price: {self.ticket_price}\nCreator ID: {self.creator_id}"

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
