import os

from dotenv import load_dotenv, find_dotenv

from flask import Flask
from flask_cors import CORS
from werkzeug.exceptions import default_exceptions

from app import config
from app.api import v1 as api_v1
from app.api.utils import error_handler

from app.ext import (
    auth,
    db,
    migrate,
    serializer
)
from app.ext.log import logger

load_dotenv(find_dotenv())

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    if config.APP_ENV != 'Testing':
        logger.info(f'Starting app in {config.APP_ENV} environment')

    if config.APP_ENV != 'Production':
        app.config["SQLALCHEMY_ECHO"] = True
        
    app.url_map.strict_slashes = False
    for code in default_exceptions:
        app.register_error_handler(code, error_handler)
    
    db.init_app(app)
    migrate.init_app(app)
    auth.init_app(app)
    serializer.init_app(app)
    CORS(app)

    api_v1.init_app(app)

    return app
