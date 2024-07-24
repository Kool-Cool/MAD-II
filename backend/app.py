from flask import Flask, redirect, url_for, flash, make_response, jsonify
from models import db, init_db
from flask_cors import CORS
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.secret_key = "your_secret_key_here"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

CORS(app)
jwt = JWTManager(app)

@app.before_request
def create_tables():
    init_db(app)

# Routes
@app.route("/home", methods=["GET", "POST"])
def home():
    return jsonify(message="This is Home")

@app.route("/logout", methods=["POST"])
def logout():
    response = make_response(redirect(url_for("home")))
    response.set_cookie('jwt', '', expires=0)  # Clear the JWT cookie
    flash("Log out successful", "success")
    return response

if __name__ == "__main__":
    app.run(debug=True)
