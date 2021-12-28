from app.models import User
from flask import jsonify, request
from functools import wraps
from app.models import User


def validate_creation(uname,role):

    user = User.query.filter_by(username=uname).first()
    if int(role) > 3 or int(role) < 0:
        return jsonify('role is not valid')

    return user

def get_final_grade(interview):
    totalmax = 0
    totalgot = 0
    for question in interview.question:
        try:
            totalmax += question.max_grade
            totalgot += question.grade
        except:
            pass
    for grade in interview.grades:
        totalgot += grade.grade
    print(f'total {totalgot} \n max: {totalmax}')
    final_grade = totalgot/totalmax/(len(interview.interviewer)+1)*100
    print(final_grade)
    interview.final_grade = final_grade

    return final_grade

def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        apikey = None
        if 'x-api-key' in request.headers:
            apikey = request.headers.get('x-api-key')
        if not apikey:
            return {'Error':'Apikey is required'}

        current_user = User.query.filter_by(private_key=apikey).first()

        if current_user is None:
            return {'Error':'Wrong apikey'}
        print(current_user)
        return f(current_user,*args,**kwargs)

    return decorated
