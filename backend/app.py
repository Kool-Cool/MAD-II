#app.py
from flask import Flask, redirect, url_for, flash, make_response, jsonify
from models import db, init_db
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from admin import admin
from sponsor import sponsor
from flask_caching import Cache

app = Flask(__name__)

app.secret_key = "your_secret_key_here"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['CACHE_TYPE'] = 'simple'
db.init_app(app)

CORS(app, resources={r"/*": {"origins": "*"}})
# CORS(app, resources={r'/*':{'origins': 'http://localhost:5173',"allow_headers": "Access-Control-Allow-Origin"}})

jwt = JWTManager(app)


app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(sponsor, url_prefix="/sponsor")


cache = Cache(app) 

@app.before_request
def create_tables():
    init_db(app)


# @cache.cached(timeout=300) # Cache for 5 minutes

# Routes
@app.route("/home", methods=["GET", "POST"])
def home():
    return jsonify(message="This is Home")

@app.route("/logout", methods=["POST","GET"])
def logout():
    response = make_response(redirect(url_for("home")))
    response.set_cookie('jwt', '', expires=0,path="/")  # Clear the JWT cookie
    flash("Log out successful", "success")
    return response


if __name__ == "__main__":
    app.run(debug=True)
