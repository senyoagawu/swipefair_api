from flask import Blueprint, request, jsonify
from app.models import db, Company, Swipe, Message, Chat, Jobseeker
# from app.models.companies import Jobseeker
# from ..auth import require_auth
bp = Blueprint("swipes", __name__, url_prefix='/api')


# posts swipe left or right via jobseeker
@bp.route('/jobseekers/<string:jobseekerEmail>/openings/<int:openingId>', methods=['POST'])
def postsJobseekerSwipes(jobseekerEmail, openingId):
    data = request.json
    jobseeker = Jobseeker.query.filter(Jobseeker.email == jobseekerEmail).one()
    jobseekerId = jobseeker.id

    swipe = Swipe(jobseekers_id=jobseekerId, openings_id=openingId, created_at='now', swiped_right=data['swiped_right'], role='jobseeker')
    db.session.add(swipe)
    db.session.commit()
    
    return swipe


# posts swipe left or right via company
@bp.route('/openings/<int:openingId>/jobseekers/<int:jobseekerId>', methods=['POST'])
def postsCompanySwipes(jobseekerId, openingId):
    data = request.json
    swipe = Swipe(jobseekers_id=jobseekerId, openings_id=openingId, created_at='now', swiped_right=data['swiped_right'], role='company')
    db.session.add(swipe)
    db.session.commit()
    return data