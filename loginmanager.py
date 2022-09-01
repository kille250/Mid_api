from flask_login import LoginManager


login_manager = LoginManager()


def create_loginmanager(app):
    login_manager.login_view = 'user_bp.login'
    login_manager.init_app(app)
