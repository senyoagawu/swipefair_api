from flask import Blueprint, request, jsonify
from app.models import db, Jobseeker
# from ..auth import require_auth_jobseeker, require_auth_company

bp = Blueprint("jobseekers", __name__, url_prefix='/api/jobseekers')

@bp.route('/')  # fetch all jobseekers
def index():
    jobseekers = Jobseeker.query.all()
    data = [jobseeker.as_dict() for jobseeker in jobseekers]
    return {'jobseekers': data}

@bp.route('/<int:jobseekerId>')  # fetch a single jobseeker
def jobseeker_id(jobseekerId):
    jobseeker = Jobseeker.query.filter(Jobseeker.id == jobseekerId).one()
    return {'jobseeker': jobseeker.as_dict()}

 
@bp.route('/<int:jobseekerId>', methods=['PUT'])  # fetch a single jobseeker
def edit_jobseeker(jobseekerId):
    data = request.json
    jobseeker = Jobseeker.query.filter(Jobseeker.id == jobseekerId).one()
    try:
        jobseeker.name = data['name'],
        jobseeker.bio = data['bio'],
        jobseeker.image = data['image'],
        jobseeker.title = data['title'],
        jobseeker.location = data['location'],
        jobseeker.education_title = data['education_title'],
        jobseeker.education_date_start = data['education_date_start'],
        jobseeker.education_date_end = data['education_date_end'],
        db.session.commit()
        return {'jobseeker': jobseeker.as_dict()}
    except AssertionError as message:
        print(str(message))
        return jsonify({"error": str(message)}), 400
