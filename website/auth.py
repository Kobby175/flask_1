from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, \
    check_password_hash  # this creates a password that is hardly to break

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(
            email=email).first()  # this is to check if the user is already in our database by filtering all the emails
        if user:
            if check_password_hash(user.password,
                                   password):  # this is to check the password of the user if it matches with that of the one in the database
                flash("logged in successfully", category='success')
                login_user(user,
                           remember=True)  # this remembers that the user has login until the user clears their browsing history or session
                # also to help flask login a user when the web restarts so that the user donot login anytime something happens
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password, try again.', category='error')
        else:
            flash('Email does not exist', category='error')
    return render_template("login.html", user=current_user)


@auth.route('/logout', methods=["GET", "POST"])
@login_required  # this makes sure that we dont logout unless the user has already login
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get('email')
        firstname = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exist.', category='success')

        elif len(email) < 4:
            flash("Email must be more than 3 characters", category='error')
        elif len(firstname) < 2:
            flash('firstname must be greater than 1 characters', category='error')
        elif password1 != password2:
            flash("Password don't match", category='error')
        elif len(password1) < 7:
            flash('password must be at least 7 characters', category='error')
        else:
            new_user = User(email=email, firstname=firstname,
                            password=generate_password_hash(password1, method='pbkdf2:sha256')
                            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account has been successfully created', category='success')
            return redirect(url_for(
                'views.home'))  # this will redirect the user to the home page. we used views.py here because we
            # already have the home functionality in the views.py,py

    return render_template("sign_up.html", user=current_user)
