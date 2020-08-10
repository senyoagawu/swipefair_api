from flask import Blueprint, request, jsonify
from app.models import db, Company, Swipe, Message, Chat, Jobseeker
# from app.models.companies import Jobseeker
# from ..auth import require_auth
bp = Blueprint("swipes", __name__, url_prefix='/api')


# posts swipe left or right via jobseeker
@bp.route('/swipes/jobseekers/<int:jobseekerId>')
def getJobseekerSwipes(jobseekerId):
    swipes = Swipe.query.filter(jobseekerId == Swipe.jobseekers_id).all()
    data = [swipe.as_dict() for swipe in swipes]
    
    return {'swipes': data}

@bp.route('/jobseekers/<int:jobseekerId>/openings/<int:openingId>', methods=['POST'])
def postsJobseekerSwipes(jobseekerId, openingId):
    data = request.json

    swipe = Swipe(jobseekers_id=jobseekerId, openings_id=openingId, created_at='now', swiped_right=data['swiped_right'], role='jobseeker')
    db.session.add(swipe)
    db.session.commit()
    
    return swipe.as_dict()


# posts swipe left or right via company
@bp.route('/openings/<int:openingId>/jobseekers/<int:jobseekerId>', methods=['POST'])
def postsCompanySwipes(jobseekerId, openingId):
    data = request.json
    swipe = Swipe(jobseekers_id=jobseekerId, openings_id=openingId, created_at='now', swiped_right=data['swiped_right'], role='company')
    db.session.add(swipe)
    db.session.commit()
    return 'data'
