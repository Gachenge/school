"""initialise the app, register all blueprints"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from web.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


mail = Mail()



def create_app(config_class=Config):
    """create the flask app with the supplied details"""
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
    from web.admin.views import admin
    from web.main.views import main
    from web.posts.views import posts
    from web.student.views import student
    from web.teacher.views import teacher
    from web.users.views import users
    
    app.register_blueprint(admin)
    app.register_blueprint(main)
    app.register_blueprint(posts)
    app.register_blueprint(student)
    app.register_blueprint(teacher)
    app.register_blueprint(users)


    return app
