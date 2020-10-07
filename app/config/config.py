import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class Config(object):
    JSON_SORT_KEYS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False    
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'static')
    PER_PAGE = os.environ.get('PER_PAGE', 10)
    MAX_ITEMS_PER_PAGE = os.environ.get('MAX_ITEMS_PER_PAGE', 100)

class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_DEV_URL')
    

class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_PROD_URL')    

class TestingConfig(Config):
    ENV = 'development'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TESTING_URL')
