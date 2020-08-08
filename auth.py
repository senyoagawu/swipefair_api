from flask import request
from functools import wraps
import jwt

from app.config import Configuration
from app.models.users import User

def require_auth_jobseeker(func):
  @wraps(func)
  def wrapped(*args, **kwargs):
    access_token = request.headers.get('Authorization', None)
    if not access_token:
      return {'error': 'authentication required'}, 401
    try:
      decoded = jwt.decode(access_token, Configuration.SECRET_KEY)
      jobseeker = Jobseeker.query.filter(Jobseeker.email == decoded.get('email')).first()
    except:
      return {'error': 'invalid auth token'}, 401
    return func(*args, authorized_user=jobseeker, **kwargs)
  return wrapped

def require_auth_company(func):
  @wraps(func)
  def wrapped(*args, **kwargs):
    access_token = request.headers.get('Authorization', None)
    if not access_token:
      return {'error': 'authentication required'}, 401
    try:
      decoded = jwt.decode(access_token, Configuration.SECRET_KEY)
      company = Company.query.filter(Company.email == decoded.get('email')).first()
    except:
      return {'error': 'invalid auth token'}, 401
    return func(*args, authorized_user=company, **kwargs)
  return wrapped
