from flask import Blueprint, request, jsonify
from app.models import db, Company, Swipe, Jobseeker
# from app.models.companies import Jobseeker
# from ..auth import require_auth
bp = Blueprint("matches", __name__, url_prefix='/api')

@bp.route('/jobseekers/<int:jobseekerId>/matches', strict_slashes=False)  # return all matched jobseekers
def jobseeker_matches(jobseekerId):
    swipesJobseeker = Swipe.query\
        .filter(Swipe.jobseekers_id == jobseekerId)\
        .filter(Swipe.role == 'jobseeker').all()
    swipesCompany = Swipe.query.filter(Swipe.jobseekers_id == jobseekerId)\
        .filter(Swipe.role == 'company').all()
    company = [s.compare() for s in swipesCompany]
    swipes = [
        swipe.opening.as_dict() 
        for swipe in swipesJobseeker 
        if swipe.compare() in 
        [s.compare() for s in swipesCompany]
    ]
    return {'matches': {'openings': swipes}}

@bp.route('/companies/<int:companyId>/matches', strict_slashes=False)  # returns the jobseekers a company has swiped on
def company_matches(companyId):
    openings = []
    companies = Company.query.filter(Company.id == companyId).all()

    _ = [openings.extend(c.openings) for c in companies]
    openingsId = [o.id for o in openings]
    swipesJobseekers = Swipe.query\
        .filter(Swipe.openings_id.in_(openingsId))\
        .filter(Swipe.role == 'jobseeker').all()
    swipesCompany = Swipe.query\
        .filter(Swipe.openings_id.in_(openingsId))\
        .filter(Swipe.role == 'company').all()
    company = [s.compare() for s in swipesCompany]
    swipes = [
        swipe.jobseeker.as_dict()
        for swipe in swipesJobseekers 
        if swipe.compare() in company]
    return {'matches': {'jobseekers': swipes}}
