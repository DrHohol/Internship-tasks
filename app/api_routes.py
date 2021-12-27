from app.models import *
from flask import request, jsonify
from flask_restful import Resource
from app.utils import valid_key, validate_creation, token_required
from app import db
from app.schema import *
import secrets
import datetime

class UserCreateApi(Resource):

    @token_required
    def post(current_user,self):

        if current_user.role != 0:
            print(current_user.role)
            return{'Error':'You are not admin'}

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

    @token_required
    def post(current_user,self):

        current_user.set_password(request.form['password'])

        return {'Success':True}


class GetInterviewsApi(Resource):

    @token_required
    def get(current_user,self):
        schema = UserSchema()
        interviews = current_user.interview
        print(interviews)
        schema = InterviewSchema(many=True)
        return jsonify({'interviews':schema.dump(interviews)})

class CreateInterviewApi(Resource):

    @token_required
    def post(current_user,self):
        schema = InterviewSchema()
        data = request.form
        interviewers = []
        
        for interviewer in data['interviewers'].split(','):
            interviewer = User.query.filter_by(username=interviewer).first()
            if interviewer is not None:
                interviewers.append(interviewer)

        recrutier = User.query.filter_by(role=1).filter_by(username=data['recrutier']).first()

        '''validate not required field "time" '''
        if data.get('time'):
            try:
                time = datetime.datetime.strptime(data.get('time'),'%H:%M').time()
            except ValueError:
                return {'Error':'Invalid time'}

        '''validate not required field "date" '''
        if data.get('date'):
            try:
                date = datetime.datetime.strptime(data.get('date'),'%d.%m.%Y')
            except ValueError:
                return {'Error':'Invalid date'}
        '''validate required fields and create Interview object'''
        try:
            interview = Interview(title=data['title'],candidat=data['candidat'],recrutier=recrutier,
                                    interviewer=interviewers,zoom_link=data.get('zoom'),time=time,date=date) #[param] for datarequired
        except KeyError:
            return {'Error':'Some data invalid'}

        print(interview)
        db.session.add(interview)
        db.session.commit()
        return jsonify(schema.dump(interview))

class GetInterviewInfoApi(Resource):

    @token_required
    def get(current_user,self):
        schema = InterviewSchema()

        interview_id = request.args['id']
        print(interview_id)
        interview = Interview.query.filter_by(id=interview_id).first()
        print(interview.recrutier)

        return jsonify(schema.dump(interview))

class GradeAnswerApi(Resource):
    
    #grade = Grades(question=quest,interview=interview,grade=form.grade.data,interviewer=current_user)
    @token_required
    def post(current_user,self):
        schema = GradeSchema()
        question = Questions.query.filter_by(id=request.form['question_id']).first()
        '''validation'''
        if question is None:
            return {'Error':'Invalid question id'}
        interview = Interview.query.filter_by(id=request.form['interview_id']).first()
        if interview is None:
            return {'Error': 'Invalid interview id'}    
        grade = int(request.form['grade'])
        if grade > question.max_grade:
            return{'Error':'Grade bigger than maximum'}

        recieved_grade = Grades(question=question,interview=interview,grade=grade,interviewer=current_user)

        db.session.add(recieved_grade)
        db.session.commit()
        return jsonify(schema.dump(recieved_grade))



