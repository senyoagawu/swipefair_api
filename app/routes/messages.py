from flask import Blueprint, request, jsonify
from app.models import db, Company, Swipe, Message, Chat
# from app.models.companies import Jobseeker
# from ..auth import require_auth
bp = Blueprint("messages", __name__, url_prefix='/api')
# fetch all jobseeker messages
@bp.route('/jobseekers/<int:jobseekerId>/chats/<int:chatId>/messages')
def grabJobseekerMessages(jobseekerId, chatId):
    currentChat = Chat.query.filter(chatId == Chat.id).one()
    if currentChat.as_dict()['jobseekers_id'] != jobseekerId:
        return '404 ERROR'
    messages = Message.query.filter(chatId == Message.chats_id).all()
    
    data = [{'message': message.as_dict()['body'], 'role': message.as_dict()['role']} for message in messages]
    return {'messages': data}

# # fetch all company messages
@bp.route('/companies/<int:companyId>/chats/<int:chatId>/messages')
def grabCompanyMessages(companyId, chatId):
    # # make sure that jobseekers id matches with chat id
    currentChat = Chat.query.filter(chatId == Chat.id).one()
    if currentChat.as_dict()['companies_id'] != companyId:
        return '404 ERROR'
    messages = Message.query.filter(chatId == Message.chats_id).all()

    data = [{'message': message.as_dict()['body'], 'role': message.as_dict()['role']} for message in messages]
    return {'messages': data}

# post a single message as a jobseeker
@bp.route('/jobseekers/<int:jobseekerId>/chats/<int:chatId>/messages', methods=['POST'])
def post_jobseeker_message(jobseekerId, chatId):
    data = request.json

    message = Message(body=data['body'], created_at='now', role='jobseeker', chats_id=chatId)
    db.session.add(message)
    db.session.commit()

    return data['body']

# # post a single message as a company
@bp.route('/companies/<int:companyId>/chats/<int:chatId>/messages', methods=['POST'])
def post_company_message(companyId, chatId):
    data = request.json

    message = Message(body=data['body'], created_at='now', role="company", chats_id=chatId)
    db.session.add(message)
    db.session.commit()

    return data['body']