from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    UserMixin, login_user, LoginManager,
    login_required, logout_user, current_user)

db = SQLAlchemy()
login_manager = LoginManager()