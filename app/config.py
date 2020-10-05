import os

class Configuration:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "postgresql://swipe_fair_user:password@localhost/swipe_fair_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "klisafluiasdfiuh"
    S3_BUCKET_NAME=os.environ.get("S3_BUCKET_NAME")
    AWS_ACCESS_KEY_ID=os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY=os.environ.get("AWS_SECRET_ACCESS_KEY")