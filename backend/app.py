from flask import Flask, jsonify
from flask_cors import CORS
# cross origin resouce sharing

app = Flask(__name__)

app.secret_key = "your_secret_key_here"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

CORS(app)

@app.route("/home", methods=["GET","POST"])
def home():
    return jsonify(message="This is Home")

if __name__ == "__main__":
    app.run(debug=True)