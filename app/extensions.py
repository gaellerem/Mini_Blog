from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_admin import Admin

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
admin = Admin(name ='', template_mode='bootstrap4')