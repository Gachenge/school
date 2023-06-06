from flask import Flask
from flask_login import LoginManager
from models import storage
import os



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'create'
    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
    app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
    

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from models.user import User

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    login_manager.login_message_category = 'info'


    @login_manager.user_loader
    def load_user(id):
        return storage.get_user_by_id(id)
    
    return app
