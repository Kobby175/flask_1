from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import Todo
views = Blueprint('views', __name__)


@views.route('/')
@login_required  # this makes sure that we dont see the homepage unless the user has already login
def home():
    user_id = current_user.id
    todos = Todo.query.filter_by(user_id=user_id).all()
    streamlit_url = f"http://localhost:8501/?user_id={user_id}"
    return render_template('home.html', streamlit_url=streamlit_url,todos=todos)


