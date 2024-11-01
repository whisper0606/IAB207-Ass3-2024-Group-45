from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, DateTimeLocalField, IntegerField, SelectField, FileField
from wtforms.validators import InputRequired, Length, Email, EqualTo, NumberRange, DataRequired

# creates the login information
class LoginForm(FlaskForm):
    email=StringField("Email", validators=[InputRequired('Enter email')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    first_name=StringField("First Name", validators=[InputRequired()])
    last_name=StringField("Last Name", validators=[InputRequired()])
    email=StringField("Email Address", validators=[Email("Please enter a valid email")])
    phone_number=IntegerField("Phone Number", validators=[InputRequired()])
    # linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")]) 
    confirm = PasswordField("Confirm Password")
    # submit button
    submit = SubmitField("Register")

class CreateEventForm(FlaskForm): # This form is for creating events
    event_name=StringField("Event Name", validators=[InputRequired()])
    event_datetime=DateTimeLocalField("Date and Time", validators=[InputRequired()])
    event_venue=StringField("Venue", validators=[InputRequired()])
    event_ticket_price=IntegerField("Ticket Price", validators=[InputRequired()])
    event_genre=SelectField("Genre", choices=[("ROCK_ALT", "Rock/Alternative"), ("POP_FOLK","Pop/Folk"), ("EDM", "Electronic/Dance"), ("HIPHOP_RNB","Hip-Hop/R&B")], validators=[InputRequired()])
    event_image=FileField("Image", validators=[DataRequired(), FileAllowed(['jpg','png','jpeg'])])
    event_artists=StringField("Artists", validators=[InputRequired()])
    create_event=SubmitField("Create Event")

class CreateCommentForm(FlaskForm):
    comment_text=StringField("Comment", validators=[InputRequired()])
    post_comment=SubmitField("Post Comment")

class PlaceOrderForm(FlaskForm):
    ticket_quantity = IntegerField("Number of Tickets", validators=[InputRequired(), NumberRange(min=1, max=10)])
    ticket_type = SelectField("Ticket Type", choices=[("NORMAL","General Admission"),("VIP","VIP")], validators=[InputRequired()])
    place_order = SubmitField("Confirm Booking")