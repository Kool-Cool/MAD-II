# backend/config.py

from flask_caching import Cache
from datetime import timedelta
from celery.schedules import crontab
from models import init_db
class Config:
    SECRET_KEY = "your_secret_key_here"
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Redis Cache configuration
    CACHE_TYPE = 'redis'
    CACHE_DEFAULT_TIMEOUT = 100
    CACHE_KEY_PREFIX = 'myprefix'
    CACHE_REDIS_URL = "redis://localhost:6379/1"
    
    # Flask-Mail configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'ojadhav@student.gitam.edu'
    MAIL_PASSWORD = 'mwrziancjfhtxvbo'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    # Celery configuration
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    CELERY_TIMEZONE = 'Asia/Kolkata'
    CELERY_BEAT_SCHEDULE = {
        'send-daily-reminders': {
            'task': 'send_daily_reminders',
            'schedule': crontab(hour=20, minute=0),  # 8 PM IST daily
        },
        'send-monthly-report': {
            'task': 'send_monthly_report',
            'schedule': crontab(day_of_month=1, hour=0, minute=0),  # Midnight on the 1st of every month
        },
    }

cache = Cache()