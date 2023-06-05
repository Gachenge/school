from flask import Flask
from flask_login import LoginManager
from models import storage



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'create'

    
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
