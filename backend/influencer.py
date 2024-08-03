# influencer.py

from flask import Blueprint, request, jsonify
from models import db, User, Sponsor, Campaign, AdRequest, Influencer, UserFlag, CampaignFlag, Negotiation
from functools import wraps
from flask_cors import cross_origin
import jwt
from datetime import datetime, timedelta
from flask_caching import Cache
import csv
from io import StringIO
from flask import Response


influencer = Blueprint("influencer", __name__)
SECRET_KEY = 'your_secret_key'
from flask_cors import cross_origin


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"message": "Token is missing!"}), 403
        try:
            token = token.split(" ")[1]  # Get token from "Bearer <token>"
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.user = data
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired!"}), 403
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token!"}), 403
        return f(*args, **kwargs)
    return decorated_function


def influencer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.user.get('role') != 'influencer':
            return jsonify({"message": "Unauthorized"}), 403
        return f(*args, **kwargs)
    return decorated_function


@influencer.route("/login",methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username = username).first()
    # print(user)

    if user and user.check_password(password):
        influencer_data = Influencer.query.filter_by(user_id = user.user_id).first()
        
        print(influencer_data.to_dict())
        
        token = jwt.encode({
            'user_id': user.user_id,
            'username': user.username,
            'role': user.role,
            'exp': datetime.utcnow() + timedelta(hours=1)
        }, SECRET_KEY, algorithm='HS256')
        return jsonify({"token": token}), 200
    return jsonify({"message": "Invalid credentials"}), 401