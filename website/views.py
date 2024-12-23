from flask import Blueprint, flash, render_template, request, url_for, redirect
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User, Event, Comment, Order
from .forms import CreateEventForm, CreateCommentForm, PlaceOrderForm
from . import db
from datetime import datetime # copied and pasted from events, need to update

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    category = request.args.get('category')
    if category:
        genre_enum = Event.Genre[category]
        events = Event.query.filter_by(genre=genre_enum).all()
    else:
        events = Event.query.limit(9).all() # retrieve up to nine events

    return render_template("index.html", events=events, Event=Event, title="MusicLIVE | Home")