import os

class Configuration:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "postgresql://swipe_fair_user:password@localhost/swipe_fair_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "klisafluiasdfiuh"
    S3_BUCKET=os.environ.get("S3_BUCKET")
    S3_KEY=os.environ.get("S3_KEY")
    S3_SECRET_ACCESS_KEY=os.environ.get("S3_SECRET_ACCESS_KEY")