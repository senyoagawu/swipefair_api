from flask import Blueprint, request, jsonify
import jwt
import json

from app.models import db, Jobseeker
from flask import Response
import jwt
# from ..models import Jobseeker
from ..config import Configuration
# from ..auth import require_auth

bp = Blueprint("session_jobseeker", __name__, url_prefix='/api/session_jobseeker')


# @bp.route('/', methods=['OPTIONS'])  # signin/start new session 
# def banana():  # to save the day from cors redirec
#     print('hello chiquita')
#     return Response(status=200) 

# so sorry, we were testing.... what were we teting

    
@bp.route('/', methods=["POST"], strict_slashes=False)  # signin/start new session 
def login():
    data = request.json
    # what's the question? currently..
    print('=====', data)
    jobseeker = Jobseeker.query.filter(Jobseeker.email == data['email']).first() #? email or Jobseekername for login
    if not jobseeker:
        return {"error": "Email not found"}, 422

    if jobseeker.check_password(data['password']) and jobseeker.is_valid_email(data['email']):
        access_token = jwt.encode({'email': jobseeker.email}, Configuration.SECRET_KEY)
        return {'access_token': access_token.decode('UTF-8'), 'jobseeker': jobseeker.as_dict()}
    else:
        return {"error": "Incorrect password"}, 401

@bp.route('/signup', methods=["POST"]) # create new account
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
    