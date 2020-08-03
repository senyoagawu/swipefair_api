from ..models import db
from .chats import Chat


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    role = db.Column(db.String(10), nullable=False)
    chats_id = db.Column(db.Integer, db.ForeignKey('chats.id'), nullable=False)

    chat = db.relationship('Chat', back_populates='messages')
