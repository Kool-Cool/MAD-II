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

from config import cache



api = Blueprint("api", __name__)
from flask_cors import cross_origin

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
@cache.cached()
@cross_origin()
def get_adrequest(ad_request_id):
    try:
        adrequest = AdRequest.query.get(ad_request_id)
        if adrequest is None:
            return jsonify({"message": "AdRequest not found", "success": False}), 404
        return jsonify(adrequest.to_dict())
    except Exception as e:
        return jsonify({"message": str(e), "success": False}), 500