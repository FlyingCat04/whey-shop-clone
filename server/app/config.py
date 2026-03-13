import os
from dotenv import load_dotenv
from urllib.parse import quote_plus, urlparse, parse_qsl, urlencode, urlunparse

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_jwt_secret")

    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DB_URL = os.getenv("DB_URL")

    password = quote_plus(os.getenv("DB_PASSWORD", ""))
    default_db_uri = f"mysql+pymysql://{DB_USER}:{password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_ENGINE_OPTIONS = {}

    # Prefer full connection string from .env. Convert mysql:// to mysql+pymysql:// for SQLAlchemy.
    if DB_URL:
        normalized_db_url = DB_URL.replace("mysql://", "mysql+pymysql://", 1)
        parsed = urlparse(normalized_db_url)
        query_params = dict(parse_qsl(parsed.query, keep_blank_values=True))

        # Convert provider-specific ssl-mode query param to PyMySQL connect args.
        ssl_mode = query_params.pop("ssl-mode", None) or query_params.pop("ssl_mode", None)
        if ssl_mode and ssl_mode.upper() == "REQUIRED":
            SQLALCHEMY_ENGINE_OPTIONS = {"connect_args": {"ssl": {}}}

        cleaned_query = urlencode(query_params)
        SQLALCHEMY_DATABASE_URI = urlunparse(parsed._replace(query=cleaned_query))
    else:
        SQLALCHEMY_DATABASE_URI = default_db_uri
        
    # Cấu hình mail
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_USERNAME")