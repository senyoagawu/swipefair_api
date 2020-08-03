from ..models import db
from .jobseekers import Jobseeker
from .companies import Company

# chats_join = db.Table(
#     'chats',
#     db.Model.metadata,
#     db.Column('jobseekers_id', db.Integer, db.ForeignKey('jobseekers.id')),
#     db.Column('companies_id', db.Integer, db.ForeignKey('companies.id'))
# )

class Chat(db.Model):
    __tablename__ = 'chats'

    id = db.Column(db.Integer, primary_key=True)
    jobseekers_id = db.Column(db.Integer, db.ForeignKey('jobseekers.id'), nullable=False)
    companies_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)

    messages = db.relationship('Message', back_populates='chat')
    company = db.relationship('Company', back_populates='chats')
    jobseeker = db.relationship('Jobseeker', back_populates='chats')