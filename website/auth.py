from flask import Blueprint, flash, render_template, request, url_for, redirect
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from .forms import LoginForm, RegisterForm
from . import db

# Create a blueprint - make sure all BPs have unique names
auth_bp = Blueprint('auth', __name__)

# register function
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    register = RegisterForm()
    #the validation of form is fine, HTTP request is POST
    if (register.validate_on_submit()==True):
            #get user's name, password, email and phone from the form
            fname = register.first_name.data
            lname = register.last_name.data
            email = register.email.data
            phone_number = register.phone_number.data
            password = register.password.data
            #check if a user exists
            user = db.session.scalar(db.select(User).where(User.email==email))
            if user:#this returns true when user is not None
                flash('Email already registered, please try another')
                return redirect(url_for('auth.register'))
            # don't store the password in plaintext!
            password_hash = generate_password_hash(password)
            #create a new User model object
            new_user = User(first_name=fname, last_name=lname, password_hash=password_hash, email=email, phone_number=phone_number)
            db.session.add(new_user)
            db.session.commit()
            #commit to the database and redirect to HTML page
            return redirect(url_for('main.index'))
    #the else is called when the HTTP request calling this page is a GET
    else:
        return render_template('register.html', form=register, heading='Register')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    error = None
    if(login_form.validate_on_submit()==True):
        #get the email and password from the database
        email = login_form.email.data
        password = login_form.password.data
        user = db.session.scalar(db.select(User).where(User.email==email))
        #if there is no user with that name
        if user is None:
            error = 'Incorrect username or password.'#changed error to reduce security risk, too lazy to change rest of code - will
        #check the password - notice password hash function
        elif not check_password_hash(user.password_hash, password): # takes the hash and password
            error = 'Incorrect username or password'
        if error is None:
            #all good, set the login_user of flask_login to manage the user
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash(error)
    return render_template('login.html', form=login_form, heading='Login')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
