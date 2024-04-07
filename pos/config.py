import os


class BaseConfig(object):
    # Change these settings as per your needs
    PROJECT = "flaskstarter"
    PROJECT_NAME = "flaskstarter.domain"
    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    BASE_URL = "https://yourdomain-flaskstarter.domain"
    ADMIN_EMAILS = ["admin@flaskstarter.domain"]

    DEBUG = False
    TESTING = False

    SECRET_KEY = "always-change-this-secret-key-with-random-alpha-nums"


class DefaultConfig(BaseConfig):

    DEBUG = True

    # Flask-Sqlalchemy
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    PG_HOST = os.getenv("PG_HOST", "localhost")
    PG_PORT = os.getenv("PG_PORT", "5432")
    PG_USER = os.getenv("PG_USER", "pos_user")
    PG_PASSWORD = os.getenv("PG_PASSWORD", "pos_password")
    PG_DB_NAME = os.getenv("PG_DB_NAME", "pos_dev")
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB_NAME}"

    PG_VECTOR_HOST = os.getenv("PG_VECTOR_HOST", "localhost")
    PG_VECTOR_PORT = os.getenv("PG_VECTOR_PORT", "5432")
    PG_VECTOR_USER = os.getenv("PG_VECTOR_USER", "pos_user")
    PG_VECTOR_PASSWORD = os.getenv("PG_VECTOR_PASSWORD", "pos_password")
    PG_VECTOR_DB_NAME = os.getenv("PG_VECTOR_DB_NAME", "pos_dev")

    # Flask-cache
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    CACHE_REDIS_PORT = os.getenv("REDIS_PORT", "6379")
    CACHE_DEFAULT_TIMEOUT = 60

    # Flask-mail
    MAIL_DEBUG = False
    MAIL_SERVER = ""  # something like 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True

    # Keep these in instance folder or in env variables
    MAIL_USERNAME = "admin-mail@yourdomain-flaskstarter.domain"
    MAIL_PASSWORD = ""
    MAIL_DEFAULT_SENDER = MAIL_USERNAME
