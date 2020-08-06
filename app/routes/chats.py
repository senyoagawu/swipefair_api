from flask import Blueprint, request, jsonify
from app.models import db, Company, Swipe, Message, Chat
# from app.models.companies import Jobseeker
# from ..auth import require_auth
bp = Blueprint("chats", __name__, url_prefix='/api')


# Grabs all of jobseekers chat
@bp.route('/jobseekers/<int:jobseekerId>/chats')
def grabJobseekerChats(jobseekerId):
    chats = Chat.query.filter(jobseekerId == Chat.jobseekers_id).all()
    # # Need .body maybe to finish up
    # data = [chat.as_dict()['companies_id'].email for chat in chats]
    data = [chat.as_dict() for chat in chats]
    return {'chats': data}


# Grabs all of companies chat
@bp.route('/companies/<int:companyId>/chats')
def grabCompanyChats(companyId):
    chats = Chat.query.filter(companyId == Chat.companies_id).all()
    # # Need .body maybe to finish up
    # data = [chat.as_dict()['companies_id'].email for chat in chats]
    data = [chat.as_dict() for chat in chats]
    return {'chats': data}


# fetch specific jobseeker chats by chatID
@bp.route('/jobseekers/<int:jobseekerId>/chats/<int:chatId>')
def grabSingleJobseekerChats(jobseekerId, chatId):
    # # # make sure that jobseekers id matches with chat id
    currentChat = Chat.query.filter(chatId == Chat.id).one()
    if currentChat.as_dict()['jobseekers_id'] != jobseekerId:
        return '404 ERROR'

    chats = Chat.query.filter(chatId == Chat.id).all()

    #TODO: need to grab name by ID instead of everything on the table
    data = [chat.as_dict() for chat in chats]
    return {'chats': data}



# fetch specific company messages chats by ChatID
@bp.route('/companies/<int:companyId>/chats/<int:chatId>')
def grabSingleCompanyChats(companyId, chatId):
    # # make sure that jobseekers id matches with chat id
    currentChat = Chat.query.filter(chatId == Chat.id).one()
    if currentChat.as_dict()['companies_id'] != companyId:
        return '404 ERROR'

    chats = Chat.query.filter(chatId == Chat.id).all()

    #TODO: need to grab name by ID instead of everything on the table
    data = [chat.as_dict() for chat in chats]
    return {'chats': data}


