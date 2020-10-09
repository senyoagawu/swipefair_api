from flask import Blueprint, request, jsonify
from app.models import db, Company, Swipe
# from app.models.companies import Jobseeker
# from ..auth import require_auth_jobseeker, require_auth_company
bp = Blueprint("companies", __name__, url_prefix='/api/companies')

@bp.route('/')  # fetch all companies
def index():
    companies = Company.query.all()
    data = [company.as_dict() for company in companies]
    return {'companies': data}

@bp.route('/<int:companyId>')  # fetch a single company
def company_id(companyId):
    company = Company.query.filter(Company.id == companyId).one()
    return {'company': company.as_dict()}


@bp.route('/<int:companyId>/notswipes/jobseekers')  #fetch  all jobseekers who have not swiped right on your openings that you haven't swiped on
def potential_jobseekers(companyId):
    jobseekers = Company.potential_jobseekers(companyId)
    return {'jobseekers': jobseekers}
