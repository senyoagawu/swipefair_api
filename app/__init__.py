from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS

from app.config import Configuration
from app.routes import jobseekers, companies, companies_session,jobseekers_session, matches, openings
from app.models import db

app = Flask(__name__)
CORS(app)  #this allows us to request info in the backend from the frontend server



app.config.from_object(Configuration)
migrate = Migrate(app, db)
db.init_app(app)

app.register_blueprint(jobseekers.bp)
app.register_blueprint(companies.bp)
app.register_blueprint(companies_session.bp)
app.register_blueprint(jobseekers_session.bp)
app.register_blueprint(matches.bp)
app.register_blueprint(openings.bp)

