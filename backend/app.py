# app.py

from flask import Flask, redirect, url_for, flash, make_response
from models import db, init_db, User
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from celery import Celery
from flask_mail import Mail
from config import cache, Config
from redis import Redis
import random

from admin import admin
from sponsor import sponsor
from influencer import influencer
from api import api

app = Flask(__name__)
app.config.from_object(Config)


db.init_app(app)
init_db(app=app)
cache.init_app(app)
jwt = JWTManager(app)
mail = Mail(app)

CORS(app, resources={r"/*": {"origins": "*"}})

app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(sponsor, url_prefix="/sponsor")
app.register_blueprint(api, url_prefix="/api")
app.register_blueprint(influencer, url_prefix="/influencer")

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    return celery

celery = make_celery(app)

redis_client = Redis(host='localhost', port=6379, db=1)
try:
    redis_client.ping()
    print("\n\nRedis connection successful\n\n")
except Exception as e:
    print(f"\n\nRedis connection failed: {e}\n\n")

@app.route("/home", methods=["GET", "POST"])
def home():
    return "Hello World! " + str(random.randint(1, 1000))

@app.route("/logout", methods=["POST", "GET"])
def logout():
    response = make_response(redirect(url_for("home")))
    response.set_cookie('jwt', '', expires=0, path="/")
    
    if app.config.get('CACHE_TYPE') == 'redis':
        prefix = app.config.get('CACHE_KEY_PREFIX', '')
        for key in redis_client.scan_iter(f"{prefix}*"):
            redis_client.delete(key)

    flash("Log out successful", "success")
    return response

if __name__ == "__main__":
    with app.app_context():
        init_db(app)
    app.run(debug=True)
