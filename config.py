import os
basedir = os.path.abspath(os.path.dirname(__file__))


SECRET_KEY = 'most-secret-key-ever'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'api_database.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
