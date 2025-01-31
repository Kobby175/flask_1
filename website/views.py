from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from .models import Todo
from . import db

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    user_id = current_user.id
    user_todos = Todo.query.filter_by(user_id=user_id).all()  # Explicitly filter by user
    streamlit_url = f"http://localhost:8501/?user_id={user_id}"
    print("Current User ID:", current_user.id)

    return render_template('home.html', streamlit_url=streamlit_url, todo=user_todos)


@views.route('/todos', methods=['GET'])
@login_required
def get_todos():
    """Fetch all todos for the logged-in user"""
    user_todos = Todo.query.filter_by(user_id=current_user.id).all()
    return jsonify([{'id': todo.id, 'data': todo.data, 'date': todo.date} for todo in user_todos])


@views.route('/add_todo', methods=['POST'])
@login_required
def add_todo():
    """Save a new todo from Streamlit into the database"""
    data = request.get_json()

    # Validate input data
    if not data or 'data' not in data:
        return jsonify({'error': 'Missing todo data'}), 400

    # Create a new Todo assigned to the logged-in user
    new_todo = Todo(data=data['data'], user_id=current_user.id)
    db.session.add(new_todo)
    db.session.commit()

    return jsonify(
        {'message': 'Todo added!', 'todo': {'id': new_todo.id, 'data': new_todo.data, 'date': new_todo.date}})
