from ..models import db
from werkzeug.security import generate_password_hash, check_password_hash


class Jobseeker(db.Model):
    __tablename__ = 'jobseekers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    hashed_password = db.Column(db.String(128), nullable=False)
    bio = db.Column(db.Text)
    image = db.Column(db.String)
    title = db.Column(db.String)
    location = db.Column(db.String)
    education_title = db.Column(db.String)
    education_date_start = db.Column(db.DateTime)
    education_date_end = db.Column(db.DateTime)

    swipes = db.relationship('Swipe', back_populates='jobseeker')
    experiences = db.relationship('Experience', back_populates='jobseeker')
    chats = db.relationship('Chat', back_populates='jobseeker')


    @property
    def password(self):
        return hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def to_dict(self):
        return {"id": self.id, "email": self.email}
