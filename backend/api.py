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

api = Blueprint("api", __name__)


@api.route("/influencers", methods=["GET"])
def get_all_influencers():
    try:
        influencers = Influencer.query.all()
        return jsonify([influencer.to_dict() for influencer in influencers])
    except Exception as e:
        
        return jsonify({"message": str(e), "success": False}), 500
    
@api.route("/campaigns", methods=["GET"])
def get_all_campaigns():
    try:
        campaigns = Campaign.query.all()
        return jsonify([campaign.to_dict() for campaign in campaigns])
    except Exception as e:
        
        return jsonify({"message": str(e), "success": False}), 500