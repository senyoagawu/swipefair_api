from ..models import db
from werkzeug.security import generate_password_hash, check_password_hash  #why dis not work?
from .jobseekers import chats_join

class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    company_name = db.Column(db.String(60), nullable=False)
    hashed_password = db.Column(db.String(128), nullable=False)
    bio = db.Column(db.Text)
    image = db.Column(db.String)
    size = db.Column(db.String(10))
    location = db.Column(db.String)

    openings = db.relationship('Opening', back_populates='company')
    chats = db.relationship('Chat', back_populates='company')
    jobseekers = db.relationship('Jobseeker', secondary=chats_join, back_populates='companies')


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
