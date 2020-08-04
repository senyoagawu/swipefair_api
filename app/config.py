import os

class Configuration:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "postgresql://swipe_fair_user:password@localhost/swipe_fair_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "klisafluiasdfiuh"