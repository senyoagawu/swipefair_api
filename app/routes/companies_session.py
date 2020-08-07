from flask import Blueprint, request, jsonify
import jwt
from app.models import db, Company
import jwt
from ..config import Configuration
# from ..auth import require_auth_jobseeker, require_auth_company

bp = Blueprint("session_companies", __name__, url_prefix='/api/session_company')

@bp.route('/', methods=["POST"])  # LOGIN/start new session 
def login():
    data = request.json
    #   print('===================', data)
    company = Company.query.filter(Company.email == data['email']).first() #? email or Companyname for login
    if not company:
        return {"error": "Email not found"}, 422

    if company.check_password(data['password']):
        access_token = jwt.encode({'email': company.email}, Configuration.SECRET_KEY)
        return {'access_token': access_token.decode('UTF-8'), 'company': company.as_dict()}
    else:
        return {"error": "Incorrect password"}, 401

@bp.route('/signup', methods=["POST"]) # create new account
def signup():
    data = request.json
    print(f"\n\n\nDATA\n{data}\n\n\n")
    company = Company(password=data['password'], email=data['email'],  company_name=data['company_name'])
    db.session.add(company)
    db.session.commit()

    access_token = jwt.encode({'email': company.email}, Configuration.SECRET_KEY)
    return {'access_token': access_token.decode('UTF-8'), 'company': company.as_dict()}

@bp.route('', methods=["DELETE"])  # LOGOUT delete current session
def logout():
    access_token = jwt.encode({'email': ''}, Configuration.SECRET_KEY)
    return {'access_token': access_token.decode('UTF-8'), 'company': ''}
    