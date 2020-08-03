from ..models import db


class Swipe(db.Model):
    __tablename__ = 'swipes'

    id = db.Column(db.Integer, primary_key=True)
    jobseekers_id = db.Column(db.Integer, db.ForeignKey('jobseekers.id'), nullable=False)
    openings_id = db.Column(db.Integer, db.ForeignKey('openings.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    swiped_right = db.Column(db.Boolean, nullable=False)
    super_swipe = db.Column(db.Boolean)
    role = db.Column(db.String(10), nullable=False)

    opening = db.relationship('Opening', back_populates='swipes')
    jobseeker = db.relationship('Jobseeker', back_populates='swipes')

