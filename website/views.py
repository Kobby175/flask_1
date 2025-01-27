from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)


@views.route('/')
@login_required  # this makes sure that we dont see the homepage unless the user has already login
def home():
    return render_template("home.html",user=current_user)
