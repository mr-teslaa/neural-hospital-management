from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_migrate import upgrade
from flask_moment import Moment
from application.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
migrate = Migrate()
moment = Moment()

login_manager.login_view = 'auth.login'

login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    migrate.init_app(app, db)

    from application.models import User
    from application.models import Role

    from application.public.views import public
    app.register_blueprint(public)

    from application.auth.views import auth
    app.register_blueprint(auth, url_prefix='/auth')

    from application.admin.views import admin
    app.register_blueprint(admin, url_prefix='/admin')

    from application.staffs.views import staffs
    app.register_blueprint(staffs, url_prefix='/staff')

    from application.users.views import users
    app.register_blueprint(users)

    return app