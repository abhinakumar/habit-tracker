import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


def _normalize_db_url(url):
    # Render (and Heroku) provide postgres:// but SQLAlchemy 1.4+/2.x requires postgresql://
    if url and url.startswith('postgres://'):
        url = url.replace('postgres://', 'postgresql://', 1)
    return url


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-this')
    SQLALCHEMY_DATABASE_URI = _normalize_db_url(
        os.environ.get('DATABASE_URL')
    ) or 'sqlite:///' + os.path.join(basedir, 'habits.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
