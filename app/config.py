import os
from dotenv import load_dotenv
load_dotenv()

class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-change-in-prod')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///quotekit.db')

class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///quotekit.db')

config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
