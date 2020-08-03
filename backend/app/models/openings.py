from ..models import db


openings_channels = db.Table(
    'openings_channels',
    db.Base.metadata,
    db.Column('channels_id', db.Integer, db.ForeignKey('channels.id')),
    db.Column('openings_id', db.Integer, db.ForeignKey('openings.id'))
)


class OpeningsChannel(db.Model):
    __tablename__ = 'channelsJesse'

    id = db.Column(db.Integer, primary_key=True)
    channels_id = db.Column(db.Integer, db.ForeignKey('channels.id'), nullable=False)
    openings_id = db.Column(db.Integer, db.ForeignKey('openings.id'), nullable=False)


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
    