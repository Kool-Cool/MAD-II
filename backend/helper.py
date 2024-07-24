# helper.py
# helper functions for database

from models import User, Campaign, Sponsor, AdRequest, Influencer, Negotiation, db
import json
from datetime import datetime
from sqlalchemy import func, case


def get_data_by_name(username):
    user = User.query.filter_by(username=username).first()
    if user is not None:
        return user.to_dict()
    else:
        return None
