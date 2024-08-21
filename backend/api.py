from flask import Blueprint, jsonify
from models import (
    User,
    Sponsor,
    Influencer,
    Campaign,
    AdRequest,
    Negotiation,
    UserFlag,
    CampaignFlag,
)
from flask import request
from models import db, Campaign
from config import cache



api = Blueprint("api", __name__)
from flask_cors import cross_origin



@api.route("/users" ,methods=["GET"])
@cache.cached()
@cross_origin()
def get_all_user():
    data = dict()

    data["admin"] = [
        user.to_dict() for user in User.query.filter_by(role="admin").all()
    ]
    data["sponsor"] = [
        user.to_dict() for user in User.query.filter_by(role="sponsor").all()
    ]
    data["influencer"] = [
        user.to_dict() for user in User.query.filter_by(role="influencer").all()
    ]

    return data

@api.route("/influencers", methods=["GET"])
@cache.cached()
@cross_origin()
def get_all_influencers():
    try:
        influencers = Influencer.query.all()
        return jsonify([influencer.to_dict() for influencer in influencers])
    except Exception as e:
        
        return jsonify({"message": str(e), "success": False}), 500


@api.route("/influencer/<int:influencer_id>", methods=["GET"])
@cache.cached()
@cross_origin()
def get_influencer(influencer_id):
    try:
        influencer = Influencer.query.get(influencer_id)
        if influencer is None:
            return jsonify({"message": "Influencer not found", "success": False}), 404
        return jsonify(influencer.to_dict())
    except Exception as e:
        return jsonify({"message": str(e), "success": False}), 500





@api.route("/campaigns", methods=["GET"])
@cache.cached()
@cross_origin()
def get_all_campaigns():
    try:
        campaigns = Campaign.query.all()
        return jsonify([campaign.to_dict() for campaign in campaigns])
    except Exception as e:
        
        return jsonify({"message": str(e), "success": False}), 500


@api.route("/campaign/<int:campaign_id>", methods=["GET"])
@cache.cached()
@cross_origin()
def get_campaign(campaign_id):
    try:
        campaign = Campaign.query.get(campaign_id)
        if campaign is None:
            return jsonify({"message": "Campaign not found", "success": False}), 404
        return jsonify(campaign.to_dict())
    except Exception as e:
        return jsonify({"message": str(e), "success": False}), 500

    


@api.route('/campaigns/public', methods=['GET'])
@cache.cached()
@cross_origin()
def get_campaigns():
    # visibility = request.args.get('visibility', 'public')  # Default to 'public'
    # search_query = request.args.get('search', '')

    # Filter campaigns based on visibility and search query
    # campaigns = db.session.query(Campaign).filter(
    #     Campaign.visibility == "public",
    #     Campaign.name.ilike(f'%{search_query}%') | Campaign.niche.ilike(f'%{search_query}%')
    # ).all()

    campaigns = db.session.query(Campaign).filter(Campaign.visibility == "public").all()

    # Convert campaigns to dictionary
    campaigns_list = [campaign.to_dict() for campaign in campaigns]
    return jsonify(campaigns_list)


@api.route("/adrequests", methods=["GET"])
@cache.cached()
@cross_origin()
def get_all_adrequests():
    try:
        adrequests = AdRequest.query.all()
        return jsonify([ad_reqst.to_dict() for ad_reqst in adrequests])
    except Exception as e:
        
        return jsonify({"message": str(e), "success": False}), 500
    
@api.route("/adrequest/<int:ad_request_id>", methods=["GET"])
@cache.cached(key_prefix='api_adrequest_data')
@cross_origin()
def get_adrequest(ad_request_id):
    try:
        adrequest = AdRequest.query.get(ad_request_id)
        if adrequest is None:
            return jsonify({"message": "AdRequest not found", "success": False}), 404
        return jsonify(adrequest.to_dict())
    except Exception as e:
        return jsonify({"message": str(e), "success": False}), 500
