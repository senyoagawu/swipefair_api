from ..models import db


class Experience(db.Model):
    __tablename__ = 'experiences'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    jobseekers_id = db.Column(db.Integer, db.ForeignKey('jobseekers.id'), nullable=False)
    date_start = db.Column(db.DateTime, nullable=False)
    date_end = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(255), nullable=False)

    jobseeker = db.relationship('Jobseeker', back_populates='experiences')
