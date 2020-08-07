from flask import Blueprint, request, jsonify
from app.models import db, Company, Swipe, Message, Chat, Experience
# from app.models.companies import Jobseeker
# from ..auth import require_auth
bp = Blueprint("experiences", __name__, url_prefix='/api/jobseekers')


# fetch all jobseeker messages
@bp.route('/<int:jobseekerId>/experiences')
def grabJobseekerExperiences(jobseekerId):
    experiences = Experience.query.filter(jobseekerId == Experience.jobseekers_id).all()

    data = [(experience.as_dict()['title'], experience.as_dict()['description'])
            for experience in experiences]
    return {'experiences': data}


@bp.route('/<int:jobseekerId>/experiences/<int:experienceId>')
def grabOneJobseekerExperiences(jobseekerId, experienceId):

    # # make sure that jobseekers id matches with experience id
    currentExperience = Experience.query.filter(experienceId == Experience.id).one()
    if currentExperience.as_dict()['jobseekers_id'] != jobseekerId:
        return '404 ERROR'

    experiences = Experience.query.filter(experienceId == Experience.id).one()
    data = [experiences.as_dict()['title'], experiences.as_dict()['description']]
    # data = [(experience.as_dict()['title'], experience.as_dict()['description'])
    #         for experience in experiences]
    return {'experiences': data}


@bp.route('/<int:jobseekerId>/experiences', methods=['POST'])
def post_jobseeker_experience(jobseekerId):
    data = request.json
    # print(f"\n\n\nDATA\n{data}\n\n\n")
    experience = Experience(title=data['title'], jobseekers_id=jobseekerId,
                            date_start=data['date_start'],  date_end=data['date_end'],
                            description=data['description'])
    db.session.add(experience)
    db.session.commit()
    # print(message.body)
    return {'experiences': [data['title'], data['description']]}


@bp.route('/<int:jobseekerId>/experiences/<int:experienceId>', methods=['PUT'])
def edit_jobseeker_message(jobseekerId, experienceId):
    data = request.json
    currentExperience = Experience.query.filter(
        experienceId == Experience.id).one()
    currentExperience.title = data['title']
    currentExperience.date_start = data['date_start']
    currentExperience.date_end= data['date_end']
    currentExperience.description = data['description']
    db.session.commit()
    return {'experiences': [data['title'], data['description']]}


@bp.route('/<int:jobseekerId>/experiences/<int:experienceId>', methods=['DELETE'])
def delete_jobseeker_message(jobseekerId, experienceId):
    currentExperience = Experience.query.filter(
        experienceId == Experience.id).one()
    db.session.delete(currentExperience)
    db.session.commit()
    return 'DELETED'
