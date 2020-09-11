from flask import Blueprint, request, jsonify
from app.models import db, Company, Swipe, Message, Chat, Jobseeker, Opening
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
    comp_info = []
    for info in data:
        company = Company.query.filter(info['companies_id'] == Company.id).one().as_dict()
        company['chatId'] = info['id']
        comp_info.append(company)
    return {'chats': comp_info}


# Grabs all of companies chat
@bp.route('/companies/<int:companyId>/chats')
def grabCompanyChats(companyId):
    chats = Chat.query.filter(companyId == Chat.companies_id).all()
    # # Need .body maybe to finish up
    # data = [chat.as_dict()['companies_id'].email for chat in chats]
    data = [chat.as_dict() for chat in chats]
    jobseeker_info = []
    for info in data:
        jobseeker = Jobseeker.query.filter(info['jobseekers_id'] == Jobseeker.id).one().as_dict()
        jobseeker['chatId'] = info['id']
        jobseeker_info.append(jobseeker)
    return {'chats': jobseeker_info}


# fetch specific jobseeker chats by chatID
@bp.route('/jobseekers/<int:jobseekerId>/chats/<int:chatId>')
def grabSingleJobseekerChats(jobseekerId, chatId):
    # # # make sure that jobseekers id matches with chat id
    currentChat = Chat.query.filter(chatId == Chat.id).one()
    if currentChat.as_dict()['jobseekers_id'] != jobseekerId:
        return '404 ERROR'

    chats = Chat.query.filter(chatId == Chat.id).one().as_dict()
    
    #TODO: need to grab name by ID instead of everything on the table
    company_id = chats['companies_id']
    company = Company.query.filter(company_id == Company.id).one().as_dict()
    return company



# fetch specific company messages chats by ChatID
@bp.route('/companies/<int:companyId>/chats/<int:chatId>')
def grabSingleCompanyChats(companyId, chatId):
    # # make sure that jobseekers id matches with chat id
    currentChat = Chat.query.filter(chatId == Chat.id).one()
    if currentChat.as_dict()['companies_id'] != companyId:
        return '404 ERROR'

    chats = Chat.query.filter(chatId == Chat.id).all()

    #TODO: need to grab name by ID instead of everything on the table
    jobseeker_id = chats['jobseekers_id']
    jobseeker = Jobseeker.query.filter(jobseeker_id == Jobseeker.id).one().as_dict()
    return jobseeker


@bp.route('/jobseekers/<int:jobseekerId>/<int:openingId>/chats', methods=['GET'])
def getJobseekerExistingChats(jobseekerId, openingId):
    # data = request.json
    companyId = Opening.query.filter(openingId == Opening.id).one().companies_id
    boolean = ''
    try:
        Chat.query.filter(jobseekerId == Chat.jobseekers_id, companyId == Chat.companies_id).one()
        boolean = True
    except:
        boolean = False
    
    return {'boolean':boolean}


@bp.route('/jobseekers/<int:jobseekerId>/<int:openingId>/chats', methods=['POST'])
def postsJobseekerNewChats(jobseekerId, openingId):
    # data = request.json
    companyId = Opening.query.filter(openingId == Opening.id).one().companies_id
    chat = Chat(jobseekers_id=jobseekerId, companies_id=companyId)
    db.session.add(chat)
    db.session.commit()

    return 'chat'


@bp.route('/companies/<int:companyId>/<int:openingId>/chats', methods=['GET'])
def getCompanyExistingChats(companyId, openingId):
    # data = request.json
    jobseekerId = Opening.query.filter(
        openingId == Opening.id).one().companies_id
    boolean = ''
    try:
        Chat.query.filter(jobseekerId == Chat.jobseekers_id,
                          companyId == Chat.companies_id).one()
        boolean = True
    except:
        boolean = False

    return {'boolean': boolean}


@bp.route('/companies/<int:companyId>/<int:openingId>/chats', methods=['POST'])
def postsCompanyNewChats(companyId, openingId):
    # data = request.json
    jobseekerId = Opening.query.filter(
        openingId == Opening.id).one().companies_id
    chat = Chat(jobseekers_id=jobseekerId, companies_id=companyId)
    db.session.add(chat)
    db.session.commit()

    return 'chat'
