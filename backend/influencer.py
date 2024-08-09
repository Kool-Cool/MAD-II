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

import helper

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
        
        # print(influencer_data.to_dict())
        
        token = jwt.encode({
            'user_id': user.user_id,
            'username': user.username,
            'role': user.role,
            'exp': datetime.utcnow() + timedelta(hours=1)
        }, SECRET_KEY, algorithm='HS256')
        return jsonify({"token": token ,  "role": user.role}), 200
    return jsonify({"message": "Invalid credentials"}), 401


@influencer.route("/register" , methods=["POST"])
def register():

    data = request.json
    #Register as User
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    role = data.get("role")

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "User already exists"}), 400
    
    new_user = User(username=username, email=email, role="influencer")
    new_user.set_password(password)

    try:
        db.session.add(new_user)
        db.session.commit()

        #Register as Influencer
        user_id = new_user.user_id
        name = data.get("name")
        category = data.get("category")
        niche = data.get("niche")
        reach = data.get("reach")

        new_influ = Influencer(
                user_id=new_user.user_id,
                category=category,
                name=name,
                niche=niche,
                reach=reach,
            )

        db.session.add(new_influ)
        db.session.commit()
        
        return jsonify({"message": "New Influencer registered successfully"}), 201
    
    except Exception as e:
        error_message = str(e).split("\n")[0]
        db.session.rollback()
        return jsonify({"message": error_message}), 400
    

@influencer.route("/dashboard", methods=["GET", "POST"])
@cross_origin()
@token_required
@influencer_required
def dashboard():
    try :
        user_id = request.user.get('user_id')
        influencer = Influencer.query.filter_by(user_id=user_id).first()

        # print(influencer)
        
        if not influencer:
            return jsonify({"message": "Influencer not found"}), 404
        
        influencer_id = influencer.influencer_id

        data = helper.get_influencer_campaigns(influencer_id)

        # print(data)
        return jsonify({"data": data}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    

@influencer.route("/acceptAdRequest/<int:ad_request_id>", methods=["POST", "GET"])
@cross_origin()
@token_required
@influencer_required
def acceptAdRqst(ad_request_id:int):
    try:
        user_id = request.user.get('user_id')
        influencer = Influencer.query.filter_by(user_id=user_id).first()

        if not influencer:
            return jsonify({"message": "Influencer not found"}), 404
        
        influencer_id = influencer.influencer_id
        ad_request_id = ad_request_id

        data = helper.get_influencer_campaigns(influencer_id)
        show_info = None
        
        for d in data:
            if d["ad_request_id"] == ad_request_id:
                show_info = d
                break


        if request.method == "POST":

            if show_info["negotiation_id"]:
                nego = Negotiation.query.filter_by(
                    negotiation_id=show_info["negotiation_id"]
                ).first()
                nego.negotiation_status = "accepted"
                nego.proposed_payment_amount = show_info["payment_amount"]

                try:
                    db.session.commit()

                except Exception as e:
                    error_message = str(e).split("\n")[0]
                    db.session.rollback()
                    return jsonify({"message": str(error_message)}), 500
            else:
                new_nego = Negotiation(
                    ad_request_id=show_info["ad_request_id"],
                    influencer_id=show_info["influencer_id"],
                    negotiation_status="accepted",
                    proposed_payment_amount=show_info["payment_amount"],
                )

                try:
                    db.session.add(new_nego)
                    db.session.commit()
                except Exception as e:
                    error_message = str(e).split("\n")[0]
                    db.session.rollback()
                    return jsonify({"message": str(error_message)}), 500


            # change ad_request status to accepted !
            ad_reqst = AdRequest.query.filter_by(
                ad_request_id=show_info["ad_request_id"]
            ).first_or_404()
            ad_reqst.status = "accepted"
            try:
                db.session.commit()

            except Exception as e:
                error_message = str(e).split("\n")[0]
                db.session.rollback()
                return jsonify({"message": str(error_message)}), 500


            return {"message" : "AD_reqest Accepted Successfully!"}
        else:
            return show_info

    except Exception as e:
        return jsonify({"message": str(e)}), 500