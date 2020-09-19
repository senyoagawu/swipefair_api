from flask import Blueprint, request, jsonify
from app.models import db, Company, Swipe, Message, Chat, Jobseeker, Opening
# from app.models.companies import Jobseeker
# from ..auth import require_auth
bp = Blueprint("swipes", __name__, url_prefix='/api')


# posts swipe left or right via jobseeker
@bp.route('/swipes/jobseekers/<int:jobseekerId>')
def getJobseekerSwipes(jobseekerId):
    swipes = Swipe.query.filter(jobseekerId == Swipe.jobseekers_id).all()
    print(swipes)
    data = [swipe.as_dict() for swipe in swipes]
    return {'swipes': data}


@bp.route('/swipes/companies/<int:companyId>')
def getCompanySwipes(companyId):
    # company = Company.query.filter(Company.id == companyId).one()
    openings = Opening.query.filter(Opening.companies_id == companyId).all()
    swipes = []
    for opening in openings:
        swipesPerOpening = Swipe.query.filter(opening.id == Swipe.openings_id).all()
        for swipe in swipesPerOpening:
            swipes.append(swipe)
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
@bp.route('/companies/<int:companyId>/openings/<int:openingId>', methods=['POST'])
def postsCompanySwipes(companyId, openingId):
    data = request.json
    jobseeker = Jobseeker.query.filter(Jobseeker.email == data['jobseekerEmail']).one()
    swipe = Swipe(jobseekers_id=jobseeker.id, openings_id=openingId, created_at='now', swiped_right=data['swiped_right'], role='company')
    db.session.add(swipe)
    db.session.commit()
    return swipe.as_dict()
