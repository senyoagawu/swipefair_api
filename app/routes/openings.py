from flask import Blueprint, request, jsonify
from app.models import db, Opening, Company
from sqlalchemy.orm import joinedload
# from app.models.opening import Opening
# from ..auth import require_auth
bp = Blueprint("openings", __name__, url_prefix='/api/openings')

@bp.route('/')  # fetch all opening
def fetchall_openings():
    companies = Company.query.all()
    openings = Opening.query.all()
    company = [c.as_dict() for c in companies]
    
    opening = [o.update(dict('company_name', o.company.name)) for o in openings]
    payload = {"opening": opening, 'company': company} # how to merge?
    return payload

@bp.route('/<int:openingId>')
def fetch_one_opening(openingId):
    opening = Opening.query.filter(Opening.id == openingId).one()
    dic = opening.as_dict()
    dic.update(opening.company.as_dict())
    return {'opening': dic}

@bp.route('/', methods=['POST'])  # fetch a single company
def post_openings(jobseekerId, chatId):
    data = request.json

    try: 
        opening = Opening(name=data['title'], type=data['title'], imgSrc=data['created_at'])
        db.session.add(opening)
        db.session.commit()
        return {"opening": opening.to_dict()}
    except AssertionError as message:
        print(str(message))
        return jsonify({"error": str(message)}), 400

@bp.route('/<int:openingId>', methods=["DELETE"])
def delete_item(openingId):
  opening = Opening.query.get(openingId)
  db.session.delete(opening)
  db.session.commit()

  return {'deletedId': itemId}

@bp.route('/<int:companyId>/notswipes/jobseekers')  #fetch  all jobseekers who have not swiped right on your openings that you haven't swiped on
def potential_jobseekers(companyId):
    return Company.potential_jobseekers(companyId)
    # return {'opens': [j.as_dict() for j in jobseekers]}