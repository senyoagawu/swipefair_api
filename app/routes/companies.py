from flask import Blueprint, request, jsonify
from app.models import db, Company, Swipe
# from app.models.companies import Jobseeker
# from ..auth import require_auth
bp = Blueprint("companies", __name__, url_prefix='/api/companies')

@bp.route('/')  # fetch all companies
def index():
    companies = Company.query.all()
    data = [company.to_dict() for company in companies]
    return {'companies': data}

@bp.route('/<int:companyId>')  # fetch a single company
def company_id(companyId):
    company = Company.query.filter(Company.id == companyId).one()
    opensId = [op.id for op in company.openings]
    swipes = Swipe.query.filter(Swipe.openings_id.in_(opensId)).all()
    swiped = [s.to_dict() for s in swipes]
    # return {'company': company.to_dict()}
    return {'opens': swiped}

@bp.route('/<int:companyId>/jobseekers')  #fetch  all jobseekers who have swiped right on your openings that you haven't swiped on
def potential_jobseekers(companyId):
    return Company.potential_jobseekers(companyId)
    # return {'opens': [j.to_dict() for j in jobseekers]}
