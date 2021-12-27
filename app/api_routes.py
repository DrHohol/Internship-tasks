from app.models import *
from flask import request, jsonify
from flask_restful import Resource
from app.utils import valid_key, validate_creation
from app import db
from app.schema import *
import secrets
import datetime

class UserCreateApi(Resource):

    def post(self):
        if not valid_key(request.headers.get('x-api-key')):
            return {'Error':'Key does not exist or expired'}
        username = request.form['username']
        firstname = request.form['First_Name']
        lastname = request.form['Last_Name']
        role = request.form['role']

        if validate_creation(username,role):
            return {'error':'Fields are not valid'}

        user = User(username=username,first_name=firstname,last_name=lastname,role=role,private_key=secrets.token_urlsafe(16))
        db.session.add(user)
        db.session.commit()

        return {'Success':True}

class SetPasswordApi(Resource):

    def post(self):

        apikey = request.headers.get('x-api-key')

        if not valid_key(apikey):
            return {'Error':'Key does not exist or expired'}

        user = User.query.filter_by(private_key=apikey).first()
        user.set_password(request.form['password'])

        return {'Success':True}


class GetInterviewsApi(Resource):

    
    def get(self):
        apikey = request.headers.get('x-api-key')
        if not valid_key(apikey):
            return {'Error':'Key does not exist or expired'}

        interviews = User.query.filter_by(private_key=apikey).first().interview
        print(interviews)
        schema = InterviewSchema(many=True)
        return jsonify({'interviews':schema.dump(interviews)})

class CreateInterviewApi(Resource):

    def post(self):
        schema = InterviewSchema()
        apikey = request.headers.get('x-api-key')
        if not valid_key(apikey):
            return {'Error':'Key does not exist or expired'}
        data = request.form
        interviewers = []
        
        for interviewer in data['interviewers'].split(','):
            interviewer = User.query.filter_by(username=interviewer).first()
            if interviewer is not None:
                interviewers.append(interviewer)

        recrutier = User.query.filter_by(role=1).filter_by(username=data['recrutier']).first()

        if data.get('time'):
            try:
                time = datetime.datetime.strptime(data.get('time'),'%H:%M').time()
            except ValueError:
                return {'Error':'Invalid time'}
        if data.get('date'):
            try:
                date = datetime.datetime.strptime(data.get('date'),'%d.%m.%Y')
            except ValueError:
                return {'Error':'Invalid date'}
        try:
            interview = Interview(title=data['title'],candidat=data['candidat'],
                                    interviewer=interviewers,zoom_link=data.get('zoom'),time=time,date=date) #[param] for datarequired
        except KeyError:
            return {'Error':'Some data invalid'}

        print(interview)
        db.session.add(interview)
        db.session.commit()
        return jsonify(schema.dump(interview))

class GetInterviewInfoApi(Resource):

    def get(self):
        schema = InterviewSchema()

        interview_id = request.args['id']
        print(interview_id)
        interview = Interview.query.filter_by(id=interview_id).first()
        print(interview.recrutier)

        return jsonify(schema.dump(interview))