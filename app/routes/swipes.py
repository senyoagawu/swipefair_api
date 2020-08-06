from flask import Blueprint, request, jsonify
from app.models import db, Company, Swipe, Message, Chat
# from app.models.companies import Jobseeker
# from ..auth import require_auth
bp = Blueprint("swipes", __name__, url_prefix='/api')


# posts swipe left or right via jobseeker
@bp.route('/jobseekers/<int:jobseekerId>/openings/<int:openingsId>', methods=['POST'])
def postsJobseekerSwipes(jobseekerId, openingsId):
    data = request.json
    # print(f"\n\n\nDATA\n{data}\n\n\n")
    swipe = Swipe(jobseekers_id=jobseekerId, openings_id=openingsId, created_at='now', swiped_right=data['swiped_right'], role='jobseeker')
    db.session.add(swipe)
    db.session.commit()
    # print(message.body)
    return data


# Grabs all of companies chat
@bp.route('/companies/<int:companyId>/openings/<int:openingsId>', methods=['POST'])
def postsCompanySwipes(companyId, openingsId):
    data = request.json
    # print(f"\n\n\nDATA\n{data}\n\n\n")
    swipe = Swipe(companies_id=companyId, openings_id=openingsId, created_at='now', swiped_right=data['swiped_right'], role='company')
    db.session.add(swipe)
    db.session.commit()
    # print(message.body)
    return data
