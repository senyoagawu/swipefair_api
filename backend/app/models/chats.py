from ..models import db
from .jobseekers import Jobseeker
from .companies import Company


class Chat(db.Model):
    __tablename__ = 'chats'

    id = db.Column(db.Integer, primary_key=True)
    jobseekers_id = db.Column(db.Integer, db.ForeignKey('jobseekers.id'), nullable=False)
    companies_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)

    messages = db.relationship('Message', back_populates='chat')
    company = db.relationship('Company', back_populates='chats')
    jobseeker = db.relationship('Jobseeker', back_populates='chats')