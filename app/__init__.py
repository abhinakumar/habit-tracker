from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config
from app.models import db, User

login_manager = LoginManager()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes.auth import auth_bp
    from app.routes.habits import habits_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(habits_bp)

    @app.route('/')
    def index():
        from flask import redirect, url_for
        from flask_login import current_user
        if current_user.is_authenticated:
            return redirect(url_for('habits.dashboard'))
        return redirect(url_for('auth.login'))

    return app
