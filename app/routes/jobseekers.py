from flask import Blueprint, request, jsonify
from app.models import db, Jobseeker
# from app.models.jobseekers import Jobseeker
# from ..auth import require_auth
bp = Blueprint("jobseekers", __name__, url_prefix='/api/jobseekers')

@bp.route('/')  # fetch all jobseekers
def index():
    # return '======================'
    jobseekers = Jobseeker.query.all()
    print(jobseekers[0].to_dict())
    data = [jobseeker.to_dict() for jobseeker in jobseekers]
    return {'jobseekers': data}

@bp.route('/<int:jobseekerId>')  # fetch a single jobseeker
def jobseeker_id(jobseekerId):
    jobseeker = Jobseeker.query.filter(Jobseeker.id == jobseekerId).one()
    # print(jobseekers[0].to_dict())
    # data = [jobseeker.to_dict() for jobseeker in jobseekers]
    return {'jobseeker': jobseeker.to_dict()}





# Lora Rusinouskaya

# # @require_auth
# def company_items_by_type(companyId, type):
#   items = Item.query.filter(Item.companyId == companyId).filter(Item.type == type.lower()).all()
#   items = [item.to_dict() for item in items]
  
#   return {"items": items}




# #! GET api/jobseekers (fetch all users)
# #! GET api/jobseekers/:id (fetch single user)
# #! GET api/companies/:id/swipes/jobseekers (the jobseekers NOT swiped on)
# #! POST api/jobseekers (create new jobseeker account)
# #! PUT api/jobseekers (edit jobseeker info)
# #! DELETE api/jobseekers/:id (delete jobseeker account)


# home
# GET api/channels/:id/jobseekers/:id/swipes/openings (the openings NOT swiped on in a channel)




# #! GET api/jobseekers (fetch all users)
# #! GET api/jobseekers/:id (fetch single user)
# #! GET api/companies/:id/swipes/jobseekers (the jobseekers NOT swiped on)
# #! POST api/jobseekers (create new jobseeker account)
# #! PUT api/jobseekers (edit jobseeker info)
# #! DELETE api/jobseekers/:id (delete jobseeker account)


# home
# GET api/channels/:id/jobseekers/:id/swipes/openings (the openings NOT swiped on in a channel)
