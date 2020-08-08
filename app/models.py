from flask_sqlalchemy import SQLAlchemy
# from validate_email import validate_email
import re #i think its a default library
# from ..models import chats, companies, experiences, jobseekers, messages, openings, swipes
from werkzeug.security import generate_password_hash, check_password_hash
# from sqlalchemy_validation import Model, Column

db = SQLAlchemy()


class MixinAsDict:
    def as_dict(self, skip=[]):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name not in skip}

#for reference
# class MixinGetByUsername:
#     username = Column(String(200), unique=True, nullable=True)
#     @classmethod
#     def get_by_username(cls, username):
#         return session.query(cls).filter(cls.username == username).first()


openings_channels = db.Table(
    'openings_channels',
    db.Model.metadata,
    db.Column('channels_id', db.Integer, db.ForeignKey('channels.id')),
    db.Column('openings_id', db.Integer, db.ForeignKey('openings.id'))
)


class Channel(MixinAsDict, db.Model):
    __tablename__ = 'channels'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    openings = db.relationship('Opening', secondary='openings_channels', back_populates='channels')


class Chat(MixinAsDict, db.Model):
    __tablename__ = 'chats'

    id = db.Column(db.Integer, primary_key=True)
    jobseekers_id = db.Column(db.Integer, db.ForeignKey('jobseekers.id'), nullable=False)
    companies_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)

    messages = db.relationship('Message', back_populates='chat')
    company = db.relationship('Company', back_populates='chats')
    jobseeker = db.relationship('Jobseeker', back_populates='chats')


class Company(MixinAsDict, db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    company_name = db.Column(db.String(60), nullable=False)
    hashed_password = db.Column(db.String(128), nullable=False)
    bio = db.Column(db.Text)
    image = db.Column(db.String, default="https://i.imgur.com/9U0akQE.png")
    size = db.Column(db.String(10))
    location = db.Column(db.String)

    openings = db.relationship('Opening', back_populates='company')
    chats = db.relationship('Chat', back_populates='company')
# my eyes aint what they used to be
    def potential_jobseekers(companyId):
        joins = Opening.query.join(Company).all()
        all_swipes = [] #bare with me
        [all_swipes.extend(swipe) for swipe in [j.swipes for j in joins]]  #ok, i notices its not actually flattened
        not_swiped = [s for s in all_swipes if not s.swiped_right]
        jobseekers = [f.jobseeker.as_dict() for f in not_swiped]
        return jobseekers  #sorry are you saying return just joins

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
    
    def is_valid_email(self, email):
        # is_valid = validate_email(self.email, check_mx=True)
        return not re.match("[^@]+@[^@]+\.[^@]+", email)


class Experience(MixinAsDict, db.Model):
    __tablename__ = 'experiences'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    jobseekers_id = db.Column(db.Integer, db.ForeignKey('jobseekers.id'), nullable=False)
    date_start = db.Column(db.DateTime, nullable=False)
    date_end = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(255), nullable=False)

    jobseeker = db.relationship('Jobseeker', back_populates='experiences')

class Jobseeker(MixinAsDict, db.Model):
    __tablename__ = 'jobseekers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    hashed_password = db.Column(db.String(128), nullable=False)
    bio = db.Column(db.Text)
    image = db.Column(db.String, default="https://i.imgur.com/kfQKjwm.png")
    title = db.Column(db.String)
    location = db.Column(db.String)
    education_title = db.Column(db.String)
    education_date_start = db.Column(db.DateTime)
    education_date_end = db.Column(db.DateTime)
    
    # is_valid = validate_email('example@example.com',check_mx=True)
    swipes = db.relationship('Swipe', back_populates='jobseeker')
    experiences = db.relationship('Experience', back_populates='jobseeker')
    chats = db.relationship('Chat', back_populates='jobseeker')
    # companies = db.relationship('Company', secondary=chats, back_populates='jobseekers')

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def is_valid_email(self, email):
        # is_valid = validate_email(self.email, check_mx=True)
        return not re.match("[^@]+@[^@]+\.[^@]+", email)

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter(cls.email == email).one()

class Message(MixinAsDict, db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    role = db.Column(db.Text, nullable=False)
    chats_id = db.Column(db.Integer, db.ForeignKey('chats.id'), nullable=False)

    chat = db.relationship('Chat', back_populates='messages')




# class OpeningsChannel(MixinAsDict, db.Model):
#     __tablename__ = 'openings_channels'

#     id = db.Column(db.Integer, primary_key=True)
#     channels_id = db.Column(db.Integer, db.ForeignKey('channels.id'), nullable=False)
#     openings_id = db.Column(db.Integer, db.ForeignKey('openings.id'), nullable=False)



class Opening(MixinAsDict, db.Model):
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
    


class Swipe(MixinAsDict, db.Model):
    __tablename__ = 'swipes'

    id = db.Column(db.Integer, primary_key=True)
    jobseekers_id = db.Column(db.Integer, db.ForeignKey('jobseekers.id'), nullable=False)
    openings_id = db.Column(db.Integer, db.ForeignKey('openings.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    swiped_right = db.Column(db.Boolean, nullable=False)
    super_swipe = db.Column(db.Boolean)
    role = db.Column(db.String)

    opening = db.relationship('Opening', back_populates='swipes')
    jobseeker = db.relationship('Jobseeker', back_populates='swipes')

    def compare(self):
        return f'{self.jobseekers_id}{self.openings_id}{self.swiped_right}'
        
