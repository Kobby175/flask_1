from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager  # this manages all  our logins

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ASDFGHJKL QWERTYUIOP'
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'  # this means my sqlachemy database is stored in sqlite
    db.init_app(app)  # this shows us that the app in the bracket is what we are going to use in the databaser5=

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import Todo, User

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_views = "auth.login" # where we should go if the user is not login
    login_manager.init_app(app)  # tells us which app we are using

    # this tells flask how we load a user
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))  # works exactly as filter but this defaultly filters only ids, and tells
        # flask what user we are looking for

    return app


# Creation of Database
def create_database(app):
    with app.app_context():
        if not path.exists('website/' + DB_NAME):
            db.create_all()
            print('Created Database!')
