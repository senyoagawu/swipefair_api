from flask import Blueprint, request, jsonify
import jwt
import json
from flask_cors import cross_origin
from werkzeug.security import generate_password_hash

from app.models import db, Jobseeker
from flask import Response
import jwt
# from ..models import Jobseeker
from ..config import Configuration
# from ..auth import require_auth

bp = Blueprint("session_jobseeker", __name__, url_prefix='/api/session_jobseeker')



    
@bp.route('/', methods=["POST"], strict_slashes=False)  # signin/start new session 
# @cross_origin()
def login():
    data = request.json
    jobseeker = Jobseeker.query.filter(Jobseeker.email == data['email']).first() #? email or Jobseekername for login
    if not jobseeker:
        return {"error": "Email not found"}, 422
    print(data['password'],jobseeker.password, generate_password_hash(data['password']))
    if jobseeker.check_password(data['password']):
        access_token = jwt.encode({'email': jobseeker.email}, Configuration.SECRET_KEY)
        return {'access_token': access_token.decode('UTF-8'), 'jobseeker': jobseeker.as_dict()}
    else:
        return {"error": "Incorrect password"}, 401

@bp.route('/signup', methods=["POST"]) # create new account
# @cross_origin()
def signup():
    data = request.json
    print(f"\n\n\nDATA\n{data}\n\n\n")
    jobseeker = Jobseeker(password=data['password'], email=data['email'], name=data['name'])
    db.session.add(jobseeker)
    db.session.commit()

    access_token = jwt.encode({'email': jobseeker.email}, Configuration.SECRET_KEY)
    return {'access_token': access_token.decode('UTF-8'), 'jobseeker': jobseeker.as_dict()}

@bp.route('', methods=["DELETE"])
def logout():
    access_token = jwt.encode({'email': ''}, Configuration.SECRET_KEY)
    return {'access_token': access_token.decode('UTF-8'), 'jobseeker': ''}
    