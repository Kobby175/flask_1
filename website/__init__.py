from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ASDFGHJKL QWERTYUIOP'
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'  # this means my sqlachemy database is stored in sqlite
    db.init_app(app)  # this shows us that the app in the bracket is what we are going to use in the database

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import Todo, User
    create_database(app)

    return app


# Creation of Database
def create_database(app):
    with app.app_context():
        if not path.exists('website/' + DB_NAME):
            db.create_all()
            print('Created Database!')