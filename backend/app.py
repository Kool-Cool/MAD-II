#app.py
from flask import Flask, redirect, url_for, flash, make_response, jsonify
from models import db, init_db
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_caching import Cache
import datetime
import time
from datetime import timedelta , timezone
import random


from config import cache  
from celery import Celery
from flask_mail import Mail,Message
from celery.schedules import crontab
from flask_caching import Cache

from admin import admin
from sponsor import sponsor
from influencer import influencer
from api import api






app = Flask(__name__)


app.secret_key = "your_secret_key_here"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_DEFAULT_TIMEOUT'] = 80
app.config["CACHE_KEY_PREFIX"] = 'myprefix'
app.config['CACHE_REDIS_URL'] = "redis://localhost:6379/1"


app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = 'your-email@example.com'
app.config["MAIL_PASSWORD"] = 'your-email-password'




CORS(app, resources={r"/*": {"origins": "*"}})
# CORS(app, resources={r'/*':{'origins': 'http://localhost:5173',"allow_headers": "Access-Control-Allow-Origin"}})




app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(sponsor, url_prefix="/sponsor")
app.register_blueprint(api, url_prefix="/api")
app.register_blueprint(influencer, url_prefix="/influencer")



def make_celery(app):
    celery = Celery(
        app.import_name,
        backend='redis://localhost:6379/0',
        broker='redis://localhost:6379/0'
    )
    celery.conf.update(app.config)
    return celery



# @app.before_request
# def create_tables():
#     init_db(app)

db.init_app(app)
cache.init_app(app) 
celery = make_celery(app)
jwt = JWTManager(app)
mail = Mail(app)






@celery.task(name="send_daily_reminders")
def send_daily_reminders():
    with app.app_context():
        # Get the current date and time in IST
        current_time = datetime.now(timezone(timedelta(hours=5, minutes=30))).replace(
            hour=20, minute=0, second=0, microsecond=0
        )

        # Get all users who have not visited the app today
        users = User.query.filter(
            or_(User.login_date == None, User.login_date < current_time)
        ).all()

        # Send emails to each user
        for user in users:
            # Create the email message
            msg = Message(
                subject="Daily Reminder: Visit the App",
                sender="your-email@example.com",
                recipients=[user.email],
            )
            msg.body = f"Dear {user.username},\n\nPlease visit the app today to enjoy the benefits."

            # Send the email
            mail.send(msg)






from redis import Redis

redis_client = Redis(host='localhost', port=6379, db=1)
try:
    redis_client.ping()
    print("\n\nRedis connection successful\n\n")
except Exception as e:
    print(f"\n\nRedis connection failed: {e}\n\n")



# Routes

@app.route("/home", methods=["GET", "POST"])
@cache.cached(timeout = 60)
def home():
    time.sleep(5)
    # return jsonify(message="This is Home")
    return "Hellow WOrld  ! " + str(random.randint(1,1000))

@app.route("/logout", methods=["POST","GET"])
def logout():
    response = make_response(redirect(url_for("home")))
    response.set_cookie('jwt', '', expires=0,path="/")  # Clear the JWT cookie
    flash("Log out successful", "success")
    return response


if __name__ == "__main__":
    app.run(debug=True)
