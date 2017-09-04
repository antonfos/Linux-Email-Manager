import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    LOGLEVEL = 2
    LOGFILE = "/var/log/mailapp.log"
    CSRF_ENABLED = True
    SECRET_KEY = '\xbbac_\x057\x8d\xe2[E\xd0\xac\xb4[\x98\x18a{\xc3i\xf0\xe7i\x19'
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_NAME = "mailserver"
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_KEY_PREFIX = "MAIL"
    SESSION_FILE_DIR = "sessions/"
    MYSQL_DATABASE_USER = 'mailadmin'
    MYSQL_DATABASE_PASSWORD = 'H6asaS6HJH6SA6D'
    MYSQL_DATABASE_DB = 'mailserver'
    MYSQL_DATABASE_HOST = 'localhost'
    ADMIN_PASSWORD = "$6$badc0e555cfbaf04$NT8vbUdLGed6jT6oDn75W33ho.aHf.1JU95Vior1mxxoKlQe/htpto62n58UvQt0TkR/ySeKc0qury8UlrPSP0"
    ADMIN_USER = "admin"

class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    LOGLEVEL = 4
    LOGFILE = "log/app.log"


class TestingConfig(Config):
    TESTING = True

