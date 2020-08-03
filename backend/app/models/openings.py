from ..models import db


openings_channels = db.Table(
    'association',
    db.Base.metadata,
    db.Column('channels_id', db.Integer, db.ForeignKey('channels.id')),
    db.Column('openings_id', db.Integer, db.ForeignKey('openings.id'))
)


class Channel(db.Model):
    __tablename__ = 'channels'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    openings = db.relationship('Opening', secondary=openings_channels, back_populates='channels')


class Opening(db.Model):
    __tablename__ = 'openings'

    id = db.Column(db.Integer, primary_key=True)
    companies_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    swipes = db.relationship('Swipe', back_populates='opening')
    company = db.relationship('Company', back_populates='openings')
    channels = db.relationship('Channel', secondary=openings_channels, back_populates='openings')