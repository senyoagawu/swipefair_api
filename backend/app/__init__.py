from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS

from app.config import Configuration
# from app.routes import items, companies, session
from app.models import db

app = Flask(__name__)
CORS(app)
app.config.from_object(Configuration)
migrate = Migrate(app, db)
db.init_app(app)

# app.register_blueprint(session.bp)

