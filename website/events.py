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

        image = form.event_image.data  # save the image to the server 
        filename = secure_filename(image.filename)
        image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        # Create the new event instance
        new_event = Event(
            name=form.event_name.data,
            datetime=form.event_datetime.data,
            venue=form.event_venue.data,
            artists=form.event_artists.data,
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
        # return redirect(url_for('main.index'))  
    
    return render_template('create_event.html', form=form, title="MusicLIVE | Create Event")  # Render the form template

@event_bp.route('/show/<int:id>', methods=['GET', 'POST'])
def show(id):
    # Fetch the event using the provided ID
    event = db.session.scalar(db.select(Event).where(Event.id == id))

    # Retrieve comments only for this event
    comments = db.session.scalars(db.select(Comment).where(Comment.event_id == id)).all()

    # Initialize the comment and booking forms
    cform = CreateCommentForm()
    bform = PlaceOrderForm()

    if cform.validate_on_submit():
        # Process the comment form
        user_id = current_user.id
        new_comment = Comment(
            text=cform.comment_text.data,
            created_at=datetime.now(),
            user_id=user_id,
            event_id=event.id 
        )
        db.session.add(new_comment)
        db.session.commit()
        flash("Comment added successfully!", "success")
        return redirect(url_for('event.show', id=event.id))

    if bform.validate_on_submit():
        # Process the booking form
        user_id = current_user.id
        ticket_type = request.form.get('ticket_type')
        new_order = Order(
            quantity=bform.ticket_quantity.data,
            type=ticket_type,
            user_id=user_id,
            event_id=event.id
        )
        db.session.add(new_order)
        db.session.commit()
        flash("Order placed successfully!", "success")
        return redirect(url_for('event.show', id=event.id))

    # Render the event details template with comments, forms, and event details
    return render_template('event_details.html', Comment=Comment, event=event, comments=comments, cform=cform, bform=bform, title="MusicLIVE | " + event.name)

@event_bp.route('/orders', methods=['GET'])
@login_required
def orders():
    # Fetch the orders for the currently logged-in user
    user_orders = db.session.scalars(db.select(Order).where(Order.user_id == current_user.id)).all()
    
    return render_template('my_bookings.html', title="MusicLIVE | My Bookings", user_orders=user_orders)
