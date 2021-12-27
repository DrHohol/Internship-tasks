from app.models import User
from flask import jsonify

def valid_key(key):

    valid = User.query.filter_by(private_key=key).first()
    
    return valid

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