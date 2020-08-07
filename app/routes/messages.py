from flask import Blueprint, request, jsonify
from app.models import db, Company, Swipe, Message, Chat
# from app.models.companies import Jobseeker
# from ..auth import require_auth
bp = Blueprint("messages", __name__, url_prefix='/api')

@bp.route('/jobseekers/<int:jobseekerId>/chats/<int:chatId>/messages')  # fetch all jobseeker messages
def grabJobseekerMessages(jobseekerId, chatId):
    # make sure that jobseekers id matches with chat id
    """
    TODO:
    """
    currentChat = Chat.query.filter(chatId == Chat.id).one()
    if currentChat.jobseeker_id != jobseekerId:
        return '404 ERROR'

    """
    TODO:
    """
    messages = Message.query.filter(chatId == Message.chats_id).all()
    data = [message.as_dict() for message in messages]  ### Need .body maybe to finish up
    return {'messages': data}

@bp.route('/companies/<int:companyId>/chats/<int:chatId>/messages>')  # fetch all company messages
def grabCompanyMessages(companyId, chatId):
    # make sure that jobseekers id matches with chat id
    """
    TODO: make sure that jobseekers id matches with chat id
    """
    currentChat = Chat.query.filter(chatId == Chat.id).one()
    if currentChat.company_id != companyId:
        return '404 ERROR'

    """
    TODO: Need .body maybe to finish up
    """
    messages = Message.query.filter(chatId == Message.chats_id).all()
    data = [message.as_dict() for message in messages]  ### Need .body maybe to finish up
    return {'messages': data}


@bp.route('/jobseekers/<int:jobseekerId>/chats/<int:chatId>/messages>', methods=['POST'])  # fetch a single company
def company_id(jobseekerId, chatId):
    data = request.json
    print(f"\n\n\nDATA\n{data}\n\n\n")
    message = Message(body=data['body'], role='jobseeker',  chats_id=chatId)
    db.session.add(message)
    db.session.commit()

@bp.route('/companies/<int:companyId>/chats/<int:chatId>/messages>', methods=['POST'])  # fetch a single company
def company_id(companyId, chatId):
    data = request.json
    print(f"\n\n\nDATA\n{data}\n\n\n")
    message = Message(body=data['body'], role='company',  chats_id=chatId)
    db.session.add(message)
    db.session.commit()