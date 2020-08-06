from flask import Blueprint, request, jsonify
from app.models import db, Jobseeker
# from app.models.jobseekers import Jobseeker
# from ..auth import require_auth
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
    try: maybe theres a better way to PUT or do you know
        jobseeker = Jobseeker.query.filter(Jobseeker.id == jobseekerId).one()
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

