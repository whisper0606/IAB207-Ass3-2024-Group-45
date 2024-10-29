from flask import Blueprint, flash, render_template, request, url_for, redirect
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User, Event
from .forms import LoginForm, RegisterForm, CreateEventForm
from . import db

event_bp = Blueprint('event', __name__)


@event_bp.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    form = CreateEventForm()
    
    if form.validate_on_submit():  # If the form is submitted and valid
        # Grab the creator_id from the currently logged-in user
        creator_id = current_user.id  
        
        # Create the new event instance
        new_event = Event(
            name=form.event_name.data,
            datetime=form.event_datetime.data,
            venue=form.event_venue.data,
            ticket_price=form.event_ticket_price.data,
            genre=form.event_genre.data,
            creator_id=creator_id
        )
        
        # Add the event to the database
        db.session.add(new_event)
        db.session.commit()
        
        flash('Event created successfully!')
        return redirect(url_for('main.index'))  # Redirect to a suitable page, like the homepage or event list
    
    return render_template('create_event_test.html', form=form)  # Render the form template

