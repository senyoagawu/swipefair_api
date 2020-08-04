from flask_sqlalchemy import SQLAlchemy
# from ..models import chats, companies, experiences, jobseekers, messages, openings, swipes

db = SQLAlchemy()


class Chat(db.Model):
    __tablename__ = 'chats'

    id = db.Column(db.Integer, primary_key=True)
    jobseekers_id = db.Column(db.Integer, db.ForeignKey('jobseekers.id'), nullable=False)
    companies_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)

    messages = db.relationship('Message', back_populates='chat')
    company = db.relationship('Company', back_populates='chats')
    jobseeker = db.relationship('Jobseeker', back_populates='chats')


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
    
    # jobseekers = db.relationship('Jobseeker', secondary=chats_join, back_populates='companies')


    @property
    def password(self):
        return hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'company_name': self.company_name,
            'bio': self.bio,
            'image': self.image,
            'size': self.size,
            'location': self.location,
        }


class Experience(db.Model):
    __tablename__ = 'experiences'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    jobseekers_id = db.Column(db.Integer, db.ForeignKey('jobseekers.id'), nullable=False)
    date_start = db.Column(db.DateTime, nullable=False)
    date_end = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(255), nullable=False)

    jobseeker = db.relationship('Jobseeker', back_populates='experiences')


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
    # companies = db.relationship('Company', secondary=chats, back_populates='jobseekers')

    @property
    def password(self):
        return hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'bio': self.bio,
            'image': self.image,
            'title': self.title,
            'location': self.location,
            'education_title': self.education_title,
            'education_date_start': self.education_date_start,
            'education_date_end': self.education_date_end,
        }


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    role = db.Column(db.String(10), nullable=False)
    chats_id = db.Column(db.Integer, db.ForeignKey('chats.id'), nullable=False)

    chat = db.relationship('Chat', back_populates='messages')


openings_channels = db.Table(
    'openings_channels',
    db.Model.metadata,
    db.Column('channels_id', db.Integer, db.ForeignKey('channels.id')),
    db.Column('openings_id', db.Integer, db.ForeignKey('openings.id'))
)


# class OpeningsChannel(db.Model):
#     __tablename__ = 'openings_channels'

#     id = db.Column(db.Integer, primary_key=True)
#     channels_id = db.Column(db.Integer, db.ForeignKey('channels.id'), nullable=False)
#     openings_id = db.Column(db.Integer, db.ForeignKey('openings.id'), nullable=False)


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
    # notswipes
    company = db.relationship('Company', back_populates='openings')
    channels = db.relationship('Channel', secondary=openings_channels, back_populates='openings')
    
    def to_dict(self):
        return {
            'id': self.id,
            'companies_id': self.companies_id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at,
        }


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

    def to_dict(self):
        return {
            'id': self.id,
            'jobseekers_id': self.jobseekers_id,
            'openings_id': self.openings_id,
            'created_at': self.created_at,
            'swiped_right': self.swiped_right,
            'super_swipe': self.super_swipe,
            'role': self.role,
        }
