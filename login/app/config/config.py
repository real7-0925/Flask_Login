#Config

import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

def create_sqlite_uri(db_name):
    return "sqlite:///" + os.path.join(basedir, db_name)

class BaseConfig:
    #基本配置
    SECRET_KEY = os.environ.get('key')
    PERMANENT_SESSION_LIFETIME = timedelta(days=14)

class DevelopmentConfig(BaseConfig):
    DEBUG = False
    SQALCHEMY_TRACK_MODIFICATIONS =False
    SQALCHEMY_DATABASE_URI = os.environ.get('db')
    SQALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 3600,
    }

class TestingConfig(BaseConfig):
    SECRET_KEY = os.urandom(24)
    TESTING =True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = create_sqlite_uri("test.db")
    WTF_CSRF_ENABLED = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}    
