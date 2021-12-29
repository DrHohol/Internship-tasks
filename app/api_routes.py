from app.models import *
from flask import request, jsonify
from flask_restful import Resource
from app.utils import validate_creation, token_required, get_final_grade, permissions_required
from app import db
from app.schema import *
import secrets
import datetime


class UserApi(Resource):

    @token_required
    @permissions_required
    def post(current_user,self):

        errors = validate_creation(request.form)
        if errors:
            return {'Error':errors}

        schema = UserSchema()
        username = request.form['username']
        firstname = request.form['First_Name']
        lastname = request.form['Last_Name']
        role = request.form['role']
        
        user = User(username=username,first_name=firstname,last_name=lastname,role=role,private_key=secrets.token_urlsafe(16))
        db.session.add(user)
        db.session.commit()

        return jsonify({'Success':True,'User':schema.dump(user)})

    @token_required
    @permissions_required
    def delete(current_user,self):

        user = User.query.filter_by(id=request.form['id'])
        if not user:
            return {'Error':'User does not exist'}

        db.session.delete(user)
        db.session.commit()

    @token_required
    @permissions_required
    def get(current_user,self):
        
        schema = UserSchema(many=True)
        users = User.query.all()

        return jsonify(schema.dump(users))


class SetPasswordApi(Resource):

    @token_required
    def post(current_user,self):

        current_user.set_password(request.form['password'])

        return {'Success':True}


class GetInterviewsApi(Resource):

    @token_required
    def get(current_user,self):
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
        questions = []
        
        for interviewer in data['interviewers'].split(','):
            interviewer = User.query.filter_by(username=interviewer).first()
            if interviewer is not None:
                interviewers.append(interviewer)

        for question in data['questions'].split(','):
            question = Questions.query.filter_by(id=question).first()
            if question:
                questions.append(question)

        recrutier = User.query.filter_by(role=2).filter_by(username=data['recrutier']).first()

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
                                    interviewer=interviewers,zoom_link=data.get('zoom'),time=time,date=date,question=questions) #[param] for datarequired
        except KeyError:
            return {'Error':'Some data invalid'}

        print(interview)
        db.session.add(interview)
        db.session.commit()
        return jsonify(schema.dump(interview))

class GetInterviewInfoApi(Resource):

    @token_required
    def get(current_user,self):

        interview_id = request.args['id']
        interview = Interview.query.filter_by(id=interview_id).first()
        if not interview:
            return {'Error':'Interview does not exist'}
        if current_user not in interview.interviewer and current_user not in [interview.recrutier]:
            return {'Error':'You are not allowed to this interview'}

        schema = InterviewSchema()

        print(interview_id)
        print(interview.recrutier)

        return jsonify(schema.dump(interview))

    @token_required   
    def delete(current_user,self):

        interview_id = request.form['id']
        interview = Interview.query.filter_by(id=interview_id).first()
        if not interview:
            return {'Error':'Interview does not exist'}
        if current_user not in interview.interviewer and current_user not in [interview.recrutier]:
            return {'Error':'You are not allowed to this interview'}
        db.session.delete(interview)
        db.session.commit()

        return {'Success':True}




class GradeAnswerApi(Resource):
    
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
        try:
            grade = int(request.form['grade'])
        except ValueError:
            return {'Error':'Grade is not a number'}
        if grade > question.max_grade:
            return{'Error':'Grade bigger than maximum'}
        '''Check user relation to interview'''
        if current_user not in interview.interviewer and current_user not in [interview.recrutier]: 
            return {'Error':'You are not allowed to this interview'}

        '''check if grade already exist'''
        a_grade = Grades.query.filter_by(
            interview_id=interview.id).filter_by(interviewer_id=current_user.id).filter_by(question_id=request.form['question_id']).first()
        if a_grade is not None:
            a_grade.grade = grade
            print(f'New grade is: {grade}')
            recieved_grade = a_grade
        else:
            recieved_grade = Grades(question=question,interview=interview,grade=grade,interviewer=current_user)
            db.session.add(recieved_grade)
        interview.final_grade = get_final_grade(interview)
        db.session.commit()
        return jsonify(schema.dump(recieved_grade))



class QuestionApi(Resource):

    @token_required
    def post(current_user,self):

        schema = QuestionSchema()
        question_text = request.form['question']
        max_grade = request.form['max_grade']
        category = Category.query.filter_by(id=request.form['category']).first()
        print(category)
        
        try:
            if category:
                question = Questions(question=question_text,max_grade=int(request.form['max_grade']),category=[category])
            else:
                question = Questions(question=question_text,max_grade=int(request.form['max_grade'])) 
        except Exception as e:
            print(e)

            return {'Error':'Invalid data'}

        db.session.add(question)
        db.session.commit()
        return jsonify(schema.dump(question))

    @token_required
    def get(current_user,self):

        schema = QuestionSchema(many=True)
        if request.args.get('all'):

            questions = Questions.query.all()
            
            return jsonify(schema.dump(questions))

        if request.args.get('category'):
            category = Category.query.filter_by(id=request.args.get('category')).first()

            return jsonify(schema.dump(category.questions))
