# sponsor.py
# Controller for sponsor login and registration....


from flask import Blueprint, request, jsonify
from models import db, User, Sponsor, Campaign, AdRequest, Influencer, UserFlag, CampaignFlag
from functools import wraps
from flask_cors import cross_origin
import jwt
from datetime import datetime, timedelta
from flask_caching import Cache

# from app import cache

sponsor = Blueprint("sponsor", __name__)
SECRET_KEY = 'your_secret_key'
# cache = Cache(config={'CACHE_TYPE': 'simple'})

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


def sponsor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.user.get('role') != 'sponsor':
            return jsonify({"message": "Unauthorized"}), 403
        return f(*args, **kwargs)
    return decorated_function



@sponsor.route("/login",methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username = username).first()
    # print(user)

    if user and user.check_password(password):
        sponsor_data = Sponsor.query.filter_by(user_id = user.user_id).first()
        
        # print(sponsor_data.to_dict())
        if sponsor and not sponsor_data.is_approved:
                return jsonify({"message": "Sponsor account is not approved yet"}), 403
        
        token = jwt.encode({
            'user_id': user.user_id,
            'username': user.username,
            'role': user.role,
            'exp': datetime.utcnow() + timedelta(hours=1)
        }, SECRET_KEY, algorithm='HS256')
        return jsonify({"token": token}), 200
    return jsonify({"message": "Invalid credentials"}), 401


@sponsor.route("/register" , methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    role = data.get("role")
    company_name = data.get("company_name")
    industry = data.get("industry")
    budget = data.get("budget")

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "User already exists"}), 400
    
    
    new_user = User(username=username, email=email, role="sponsor")
    new_user.set_password(password)

    try:
            db.session.add(new_user)
            db.session.commit()

            new_sponsor = Sponsor(
                user_id=new_user.user_id,
                company_name=company_name,
                industry=industry,
                budget=budget,
            )
            db.session.add(new_sponsor)
            db.session.commit()
            return jsonify({"message": "New Sponsor registered successfully"}), 201

    except Exception as e:
        error_message = str(e).split("\n")[0]
        db.session.rollback()
        return jsonify({"message": error_message}), 400

    
@sponsor.route("/dashboard/data", methods=["GET"])
@cross_origin()
@token_required
@sponsor_required
def dashboard_data():
    try:
        # Extract the user information from the request context (set by token_required)
        user_id = request.user.get('user_id')

        # Fetch the sponsor's record based on the user_id
        sponsor = Sponsor.query.filter_by(user_id=user_id).first()

        if not sponsor:
            return jsonify({"message": "Sponsor not found"}), 404

        # Fetch campaigns associated with the sponsor's sponsor_id
        campaigns = Campaign.query.filter_by(sponsor_id=sponsor.sponsor_id).all()

        # Serialize campaign data
        campaign_data = [campaign.to_dict() for campaign in campaigns]
        # print(campaign_data)
        return jsonify({"campaigns": campaign_data}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500
    


@sponsor.route("/addcampaign", methods=["POST"])
@cross_origin()
@token_required
@sponsor_required
def add_campaign():
    data = request.json
    try:
        user_id = request.user.get('user_id')
        sponsor_data = Sponsor.query.filter_by(user_id=user_id).first()
        if not sponsor_data:
            return jsonify({"message": "Sponsor not found"}), 404
        
        new_campaign = Campaign(
            sponsor_id=sponsor_data.sponsor_id,
            name=data.get("name"),
            description=data.get("description"),
            start_date=datetime.strptime(data.get("startDate"), "%Y-%m-%d").date(),
            end_date=datetime.strptime(data.get("endDate"), "%Y-%m-%d").date(),
            budget=data.get("budget"),
            visibility=data.get("visibility"),
            goals=data.get("goals"),
            niche=data.get("niche"),
        )

        db.session.add(new_campaign)
        db.session.commit()
        return jsonify({"message": "New campaign added successfully", "success": True}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e), "success": False}), 500