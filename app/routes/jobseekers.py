from flask import Blueprint, request, jsonify
from app.models import db, Jobseeker, Opening
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


@bp.route('/<int:jobseekerId>/notswipes/openings')
def not_already_swiped_openings(jobseekerId):
    openings = Opening.query.all()
    # openings where jobseeker is not in swiped
    openingsids = []
    _ = [openingsids.extend(o.swipes) for o in openings]

    unswipedOpenigns = Opening.query.filter(Opening.id.notin_([o.openings_id for o in openingsids])).all()
    # all_jobseekers_id = [all]
    print(unswipedOpenigns)
    return {'Openings': [u.as_dict() for u in unswipedOpenigns]}
