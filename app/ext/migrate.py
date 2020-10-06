from flask_migrate import Migrate

from app.ext.db import db
from app.api import models

migrate = Migrate()

def init_app(app):
    migrate.init_app(app, db)