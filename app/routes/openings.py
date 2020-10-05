from flask import Blueprint, request, jsonify
from app.models import db, Opening, Company, Jobseeker
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
  
    openings_info = [] 

    for info in data:
        company = Company.query.filter(info['companies_id'] == Company.id).one().as_dict()
        openingsAndCompaniesInfo = {}
        openingsAndCompaniesInfo['id'] = info['id']
        openingsAndCompaniesInfo['image'] = company['image']
        openingsAndCompaniesInfo['company_name'] = company['company_name']
        openingsAndCompaniesInfo['email'] = company['email']
        openingsAndCompaniesInfo['size'] = company['size']
        openingsAndCompaniesInfo['location'] = company['location']
        openingsAndCompaniesInfo['bio'] = company['bio']
        openingsAndCompaniesInfo['title'] = info['title']
        openingsAndCompaniesInfo['description'] = info['description']
        openings_info.append(openingsAndCompaniesInfo)
    # o for o in openings

# c1 = session.query(Customer).options(joinedload(Customer.invoices)).filter_by(name='Govind Pant').one()
# c1 = db.session.query(Company).options(joinedload(.invoices)).filter_by(name='Govind Pant').one()
    
    # opening = [o.update(dict('company_name', o.company.name)) for o in openings]
    # opening = [o.as_dict() for o in openings]
    payload = {"opening": openings_info} # how to merge?
    return payload

@bp.route('/<int:openingId>')
def fetch_one_opening(openingId):
    opening = Opening.query.filter(Opening.id == openingId).one()
    dic = opening.as_dict()
    dic.update(opening.company.as_dict())
    return {'opening': dic}

@bp.route('/notswiped/jobseeker/<int:jobseekerId>') #openings you haven't swiped on
def opening_not_swiped(jobseekerId):
    companies = Company.query.all()
    jobseeker = Jobseeker.query.filter(Jobseeker.id == jobseekerId).one()
    swipes = [ j for j in jobseeker.swipes]
    jobseeker_swipes = [s for s in swipes if s.role == 'jobseeker']
    openingsId = [s.opening.id for s in jobseeker_swipes]
    openings = Opening.query.filter(Opening.id.notin_(openingsId)).all()
    print(openings)
    company = [c.as_dict() for c in companies]
    data = [opening.as_dict() for opening in openings]
    openings_info = [] 

    for info in data:
        company = Company.query.filter(info['companies_id'] == Company.id).one().as_dict()
        openingsAndCompaniesInfo = {}
        openingsAndCompaniesInfo['id'] = info['id']
        openingsAndCompaniesInfo['image'] = company['image']
        openingsAndCompaniesInfo['name'] = company['company_name']
        openingsAndCompaniesInfo['email'] = company['email']
        openingsAndCompaniesInfo['size'] = company['size']
        openingsAndCompaniesInfo['location'] = company['location']
        openingsAndCompaniesInfo['bio'] = company['bio']
        openingsAndCompaniesInfo['title'] = info['title']
        openingsAndCompaniesInfo['description'] = info['description']
        openings_info.append(openingsAndCompaniesInfo)

    payload = {"opening": openings_info} # how to merge?
    return payload

@bp.route('/companies/<int:companyId>', methods=['POST'])  # post a new opening
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

@bp.route('/companies/<int:companyId>', methods=['POST'])  # post a new opening
def post_companies(companyId):
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

# @bp.route('/<int:companyId>/notswipes/jobseekers')  #fetch  all jobseekers who have not swiped right on your openings that you haven't swiped on
# def potential_jobseekers(companyId):
#     return {'jobseekers': Company.potential_jobseekers(companyId)}


@bp.route('/notswiped/company/<int:companyId>')
def potential_jobseekers(companyId):

    jobseekers = Jobseeker.query.all()
    company = Company.query.filter(Company.id == companyId).one()
    openings = Opening.query.filter(Opening.companies_id == companyId).all()
    swipes = []
    for opening in openings:
        for swipesPerOpening in opening.swipes:
            swipes.append(swipesPerOpening)
    company_swipes = [s for s in swipes if s.role == 'company']
    jobseekersId = [s.jobseeker.id for s in company_swipes]
    jobseekersList = Jobseeker.query.filter(Jobseeker.id.notin_(jobseekersId)).all()
    # openings = Opening.query.filter(Opening.id.notin_(openingsId)).all()
    jobseeker = [j.as_dict() for j in jobseekersList]
    data = [opening.as_dict() for o in openings]
    # print(data)
    # print(jobseeker)

    jobseekers_info = []
    
    for info in jobseeker:
        # print('hi')
        openings = Opening.query.filter(Opening.companies_id == companyId).all()
        for opening in openings:
            openingsAndJobseekersInfo = {}
            openingsAndJobseekersInfo['id'] = opening.as_dict()['id']
            openingsAndJobseekersInfo['image'] = info['image']
            openingsAndJobseekersInfo['name'] = info['name']
            openingsAndJobseekersInfo['email'] = info['email']
            openingsAndJobseekersInfo['size'] = info['education_title']
            openingsAndJobseekersInfo['location'] = info['location']
            openingsAndJobseekersInfo['bio'] = info['bio']
            openingsAndJobseekersInfo['title'] = opening.as_dict()['title']
            openingsAndJobseekersInfo['description'] = opening.as_dict()['description']
            jobseekers_info.append(openingsAndJobseekersInfo)
    
    payload = {"jobseekers": jobseekers_info}  # how to merge?
    # print(payload)
    return payload
    # return {'jobseekers': Company.potential_jobseekers(companyId)}
