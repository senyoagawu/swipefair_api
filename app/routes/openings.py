from flask import Blueprint, request, jsonify
from app.models import db, Opening, Company
from sqlalchemy.orm import joinedload, subqueryload
# from app.models.opening import Opening
# from ..auth import require_auth
bp = Blueprint("openings", __name__, url_prefix='/api/openings')

@bp.route('/')  # fetch all opening
def fetchall_openings():
    companies = Company.query.all()
    openings = Opening.query.all()
    company = [c.as_dict() for c in companies]
    data = [opening.as_dict() for opening in openings]
    opening_info = []

    for info in data:
        company = Company.query.filter(info['companies_id'] == Company.id).one().as_dict()
        openingAndCompanyInfo = {}
        openingAndCompanyInfo['image'] = company['image']
        openingAndCompanyInfo['company_name'] = company['company_name']
        openingAndCompanyInfo['email'] = company['email']
        openingAndCompanyInfo['size'] = company['size']
        openingAndCompanyInfo['location'] = company['location']
        openingAndCompanyInfo['bio'] = company['bio']
        openingAndCompanyInfo['title'] = info['title']
        openingAndCompanyInfo['description'] = info['description']
        opening_info.append(openingAndCompanyInfo)
    # o for o in openings

# c1 = session.query(Customer).options(joinedload(Customer.invoices)).filter_by(name='Govind Pant').one()
# c1 = db.session.query(Company).options(joinedload(.invoices)).filter_by(name='Govind Pant').one()
    
    # opening = [o.update(dict('company_name', o.company.name)) for o in openings]
    # opening = [o.as_dict() for o in openings]
    payload = {"opening": opening_info} # how to merge?
    return payload

@bp.route('/<int:openingId>')
def fetch_one_opening(openingId):
    opening = Opening.query.filter(Opening.id == openingId).one()
    dic = opening.as_dict()
    dic.update(opening.company.as_dict())
    return {'opening': dic}


@bp.route('companies/<int:companyId>', methods=['POST'])  # post a new opening
def post_openings(companyId):
    data = request.json

    try:
        opening = Opening(
            companies_id=companyId, title=data['title'], description=data['description'], created_at='now')
        db.session.add(opening)
        db.session.commit()
        return {"opening": opening.as_dict()}
    except AssertionError as message:
        print(str(message))
        return jsonify({"error": str(message)}), 400

@bp.route('/<int:openingId>', methods=["DELETE"])
def delete_item(openingId):
    opening = Opening.query.get(openingId)
    db.session.delete(opening)
    db.session.commit()
    return {'deletedId': openingId}

@bp.route('/<int:companyId>/notswipes/jobseekers')  #fetch  all jobseekers who have not swiped right on your openings that you haven't swiped on
def potential_jobseekers(companyId):
    return {'jobseekers': Company.potential_jobseekers(companyId)}
