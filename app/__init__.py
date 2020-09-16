from flask import Flask, request
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin
import boto3

from app.config import Configuration
from app.routes import jobseekers, companies, companies_session,jobseekers_session, messages, chats, swipes, experiences, matches, openings
from app.models import db

s3_resource = boto3.resource(
    "s3", 
    aws_access_key_id=Configuration.S3_KEY,
    aws_secret_access_key=Configuration.S3_SECRET_ACCESS_KEY
)

app = Flask(__name__)
CORS(app, support_credentials=True)  # this allows us to request info in the backend from the frontend server
# app.config['CORS_HEADERS'] = 'Content-Type'

# def add_cors_headers(response):
#     response.headers['Access-Control-Allow-Origin'] = '*'
#     if request.method == 'OPTIONS':
#         response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
#         headers = request.headers.get('Access-Control-Request-Headers')
#         if headers:
#             response.headers['Access-Control-Allow-Headers'] = headers
#     return response


# app.after_request(add_cors_headers)

app.config.from_object(Configuration)
db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(jobseekers.bp)
app.register_blueprint(companies.bp)
app.register_blueprint(companies_session.bp)
app.register_blueprint(jobseekers_session.bp)
app.register_blueprint(messages.bp)
app.register_blueprint(chats.bp)
app.register_blueprint(swipes.bp)
app.register_blueprint(experiences.bp)
app.register_blueprint(matches.bp)
app.register_blueprint(openings.bp)

