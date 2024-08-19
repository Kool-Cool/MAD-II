from flask import Blueprint, request, jsonify
from models import db, User, Sponsor, Campaign, AdRequest, Influencer, UserFlag, CampaignFlag
from functools import wraps
from flask_cors import cross_origin
import jwt
from datetime import datetime, timedelta

from config import cache

admin = Blueprint("admin", __name__)
SECRET_KEY = 'your_secret_key'


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


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.user.get('role') != 'admin':
            return jsonify({"message": "Unauthorized"}), 403
        return f(*args, **kwargs)
    return decorated_function


@admin.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        token = jwt.encode({
            'user_id': user.user_id,
            'username': user.username,
            'role': user.role,
            'exp': datetime.utcnow() + timedelta(hours=1)
        }, SECRET_KEY, algorithm='HS256')
        user.login_date = datetime.utcnow()
        db.session.commit()
        return jsonify({"token": token ,  "role": user.role}), 200
    return jsonify({"message": "Invalid credentials"}), 401


@admin.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    role = data.get("role")

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "User already exists"}), 400

    new_user = User(username=username, email=email, role=role)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@admin.route("/dashboard/data", methods=["GET"])
@cross_origin()
@token_required
@admin_required
@cache.cached(key_prefix='dashboard_data')
def dashboard_data():
    try:
        data = {
            "total_users": User.query.count(),
            "total_sponsors": Sponsor.query.count(),
            "total_campaigns_public": Campaign.query.filter_by(visibility="public").count(),
            "total_campaigns_private": Campaign.query.filter_by(visibility="private").count(),
            "total_ad_requests_pending": AdRequest.query.filter_by(status="pending").count(),
            "total_ad_requests_rejected": AdRequest.query.filter_by(status="rejected").count(),
            "total_ad_requests_negotiation": AdRequest.query.filter_by(status="negotiation").count(),
            "total_ad_requests_accepted": AdRequest.query.filter_by(status="accepted").count(),
            "total_influencers": Influencer.query.count(),
            "flagged_users": UserFlag.query.count(),
            "flagged_campaigns": CampaignFlag.query.count(),
            "pending_sponsors": Sponsor.query.filter_by(is_approved=False).count()  # Count pending sponsors
        }
        # print(data)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@admin.route("/pending_sponsors", methods=["GET"])
@token_required
@admin_required
@cache.cached()
def pending_sponsors():
    try:
        sponsors = Sponsor.query.filter_by(is_approved=False).all()
        return jsonify([sponsor.to_dict() for sponsor in sponsors])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@admin.route("/approve_sponsor/<int:sponsor_id>", methods=["POST"])
@token_required
@admin_required
def approve_sponsor(sponsor_id):
    try:
        sponsor = Sponsor.query.get(sponsor_id)
        if not sponsor:
            return jsonify({"message": "Sponsor not found"}), 404
        sponsor.is_approved = True
        db.session.commit()

        cache.delete('dashboard_data')
        return jsonify({"message": "Sponsor approved successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@admin.route("/flag_user", methods=["POST"])
@token_required
@admin_required
def flag_user():
    data = request.json
    user_id_to_flag = data.get("user_id")
    reason = data.get("reason")

    if request.user['user_id'] == user_id_to_flag:
        return jsonify({"message": "You cannot flag yourself"}), 403

    user_to_flag = User.query.get(user_id_to_flag)
    if not user_to_flag:
        return jsonify({"message": "User not found"}), 404

    flag = UserFlag(
        flagged_by=request.user['user_id'],
        user_id=user_id_to_flag,
        reason=reason
    )

    try:
        db.session.add(flag)
        db.session.commit()
        cache.delete('dashboard_data')
        return jsonify({"message": "User flagged successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500