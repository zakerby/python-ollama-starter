from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_login import LoginManager

db = SQLAlchemy()
cache = Cache()

login_manager = LoginManager()

