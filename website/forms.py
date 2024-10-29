from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, DateTimeLocalField, IntegerField, SelectField, FileField
from wtforms.validators import InputRequired, Length, Email, EqualTo

# creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired()])
    email = StringField("Email Address", validators=[Email("Please enter a valid email")])
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
    event_genre=SelectField("Genre", choices=[("ROCK_ALT", "Rock/Alternative"), ("POP","Pop"), ("EDM", "Electronic/Dance"), ("HIPHOP_RNB","Hip-Hop/R&B")], validators=[InputRequired()])
    event_image=FileField("Image", render_kw={"disabled": True}) # File uploads disabled because i'm a lazy fuck - will :)
    create_event=SubmitField("Create Event")

class CreateCommentForm(FlaskForm):
    comment_text=StringField("Comment", validators=[InputRequired()])
    post_comment=SubmitField("Post Comment")