from app import app, db
from flask import render_template, flash, redirect, url_for, request, jsonify
from werkzeug.urls import url_parse
from app.forms import *
from app.models import User, Questions, Interview, Category, Grades
from flask_login import current_user, login_user, logout_user, login_required
import secrets
from app.schema import *
from app.utils import valid_key, get_final_grade

'''
Accept:application/json
if request.headers.get('Accept') == 'application/json':
    #{'experts':[recrutier.username for recrutier in User.query.filter_by(role=1).all()]}

    key = request.headers.get('x-api-key')
    if valid_key(key):
        users = User.query.filter_by(private_key=key ).first()
        print(users)
        user_schema = UserSchema()
        return jsonify(user_schema.dump(users))
    else:
        return jsonify({'Error':'Key does not exist'})
'''

@app.route('/')
def index():

    return render_template('index.html',title='WELCOME')


@app.route('/my-interviews',)
@login_required
def interviews():

    return render_template('interviews.html',title='My Interviews')

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user,remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        flash('Login requested for user {} remember me is {}'.format(form.username.data,form.remember_me.data))
        return redirect(next_page)
    
    return render_template('login.html',title='Sign In',form=form)


@app.route('/create-interview',methods=['GET','POST'])
@login_required
def create_interview():

    
    form = InterviewCreationForm()
    ''' add choices to select fields '''
    form.recrutier.choices = [recrutier.username for recrutier in User.query.filter_by(role=2).all()]
    form.experts.choices = [(expert.id, expert.username) for expert in User.query.filter_by(role=1).all()]
    form.questions.choices = [(question.id, question.question) for question in Questions.query.all()]
    if form.validate_on_submit():

        ''' create list of questions '''
        qlist = []
        for i in form.questions.data:
            question = Questions.query.filter_by(id=i).first()
            qlist.append(question)

        ''' creating list of experts '''
        elist = []
        for expert in form.experts.data:
            exp = User.query.filter_by(id=expert).first()
            elist.append(exp)

        inter = Interview(title=form.interview_title.data,candidat=form.candidat_name.data,
                        recrutier=User.query.filter_by(username=form.recrutier.data).first(),
                        question=qlist, interviewer=elist,zoom_link=form.zoom.data,
                        date=form.date.data,time=form.time.data)
        db.session.add(inter)
        db.session.commit()
        flash('Interview created successfuly')
    else:
        print(form.errors)

    return render_template('create_interview.html',form=form )

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/create-question',methods=['GET',"POST"])
@login_required
def create_question():

    form = QuestionCreateForm()
    form.category.choices = [(category.id, category.name) for category in Category.query.all()]
    if form.validate_on_submit():
        new_question = Questions(question=form.question.data,max_grade=form.max_grade.data)

        db.session.add(new_question)
        db.session.commit()
        flash('Question created successfuly')

    return render_template('create_question.html',form=form)

@login_required
@app.route('/interview/<interview_id>',methods=['GET','POST'])
def interview(interview_id):

    interview = Interview.query.filter_by(id=interview_id).first()
    if current_user not in interview.interviewer and current_user not in [interview.recrutier]:

        return redirect(url_for('index'),code=302)

    form = GradeInterviewForm()
  # form.questions = [question for question in Questions.query.all() if question.interviews.id == interview.id]
    print(interview.question)
    for q in interview.question:
        try:
            form.question.choices.append((q.id,q.question))
        except AttributeError as e:
            print(e)
            pass

    if form.validate_on_submit():
        quest = Questions.query.filter_by(id=form.question.data).first()
        grade = Grades.query.filter_by(interview_id=interview_id).filter_by(interviewer_id=current_user.id).filter_by(question_id=quest.id).first()
        print(grade)
        if grade is not None:
            grade.grade = form.grade.data
            print(f'New grade is: {grade}')
        else:
            grade = Grades(question=quest,interview=interview,grade=form.grade.data,interviewer=current_user)
        db.session.add(grade)

       
        interview.final_grade = get_final_grade(interview)
        db.session.commit()
    else:
        print(form.errors)


    return render_template('interview.html',title="interview",interview=interview,form=form)

@app.route('/set-password',methods=['GET','POST'])
def set_password():
    pkey = request.args.get('key')
    print(pkey)
    if pkey == None:
        redirect(url_for('index'))
    form = SetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(private_key=pkey).first()
        if user == None:
            flash('key does not exist')
        user.set_password(form.password.data)
        user.private_key = secrets.token_urlsafe(16)
        db.session.add(user)
        db.session.commit()

    return render_template('set_password.html',form=form)


@app.route('/create-user',methods=['GET','POST'])
@login_required
def create_user():
    form = CreateUserForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,first_name=form.firstname.data,last_name=form.lastname.data,
                    private_key=secrets.token_urlsafe(16),role=form.role.data)
        db.session.add(user)
        db.session.commit()
        flash('User created successfuly!')

    return render_template('create_user.html',title='Create new user',form=form)