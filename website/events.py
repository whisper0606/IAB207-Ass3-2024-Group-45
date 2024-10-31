from flask import Blueprint, flash, render_template, request, url_for, redirect, current_app
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User, Event, Comment, Order
from .forms import CreateEventForm, CreateCommentForm, PlaceOrderForm
from . import db
from werkzeug.utils import secure_filename
from datetime import datetime 
import os

event_bp = Blueprint('event', __name__)


@event_bp.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    form = CreateEventForm()
    
    if form.validate_on_submit():  # If the form is submitted and valid
        # Grab the creator_id from the currently logged-in user
        creator_id = current_user.id  # get the user id from the session

        image=form.event_image.data # save the image to the server 
        print(type(image))
        filename=secure_filename(image.filename)
        image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        
        # Create the new event instance
        new_event = Event(
            name=form.event_name.data,
            datetime=form.event_datetime.data,
            venue=form.event_venue.data,
            ticket_price=form.event_ticket_price.data,
            genre=form.event_genre.data,
            status="OPEN",
            image=filename,
            creator_id=creator_id
        )
        
        # Add the event to the database
        db.session.add(new_event)
        db.session.commit()
        
        flash('Event created successfully!')
        return redirect(url_for('main.index'))  # Redirect to a suitable page, like the homepage or event list
    
    return render_template('create_event.html', form=form)  # Render the form template

@event_bp.route('/comment', methods=['GET','POST']) # This is going to need to be replaced and linked to events, hopefully this will be somewhat useful
@login_required
def comment():
    form = CreateCommentForm()

    if form.validate_on_submit():
        user_id = current_user.id # take the user ID from the session
        new_comment = Comment(
            text=form.comment_text.data,
            created_at=datetime.now(),
            user_id=user_id,
            event_id=1 # event ID set to 1 for now, since comments aren't linked to events yet
        )

        db.session.add(new_comment)
        db.session.commit()
        flash("comment added", "success")
    return render_template('form_test.html', form=form)

@event_bp.route('/order', methods=['GET','POST'])
@login_required
def order():
    form = PlaceOrderForm()

    if form.validate_on_submit():
        user_id = current_user.id
        new_order = Order(
            quantity=form.ticket_quantity.data,
            type=form.ticket_type.data,
            user_id=user_id,
            event_id=1 # set to one for testing purposes, please change once you link orders to events :)
        )

        db.session.add(new_order)
        db.session.commit()
        flash("order placed", "success")
    return render_template("form_test.html", form=form)



