from app import db, login, admin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_admin.contrib.sqlamodel import ModelView


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


question_indef = db.Table('question_indentif',
    db.Column('question_id',db.Integer,db.ForeignKey('questions.id'),primary_key=True),
    db.Column('interview_id',db.Integer,db.ForeignKey('interview.id'),primary_key=True))

expert_ident = db.Table('expert_ident',
    db.Column('expert_uname',db.String,db.ForeignKey('user.username'),primary_key=True),
    db.Column('interview_id',db.Integer,db.ForeignKey('interview.id'),primary_key=True))

category_ident = db.Table('category_ident',
    db.Column('question_id',db.Integer,db.ForeignKey('questions.id'),primary_key=True),
    db.Column('category_id',db.Integer,db.ForeignKey('category.id'),primary_key=True))


class User(db.Model,UserMixin):
    '''Table for user'''
    private_key = db.Column(db.String(24),unique=True)
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),index=True,unique=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    role = db.Column(db.Integer)
    password_hash = db.Column(db.String(256))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):

        return self.username

class Interview(db.Model):

    id = db.Column(db.Integer,primary_key=True) 
    title = db.Column(db.String(64))
    recrutier = db.Column(db.String(64), db.ForeignKey('user.username'))
    
    question = db.relationship('Questions',backref=db.backref('interviews',lazy=True),
                                lazy='subquery',secondary=question_indef)
    interviewer = db.relationship('User',backref=db.backref('interview'),lazy='subquery',secondary=expert_ident)
    candidat = db.Column(db.String)
    final_grade = db.Column(db.Integer)
    zoom_link = db.Column(db.String)
    date = db.Column(db.Date)
    time = db.Column(db.Time)

    def __repr__(self):

        return 'Interview {} with {}'.format(self.title,self.candidat)

    def get_url(self):

        return self.id

class Questions(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    question = db.Column(db.String(128))
    grade = db.Column(db.Integer)
    max_grade = db.Column(db.Integer)
    category = db.relationship('Category',backref='questions',lazy=True,secondary=category_ident)

    def __repr__(self):

        return f'{self.question}'

class Grades(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    question_id = db.Column(db.Integer,db.ForeignKey('questions.id'))
    question = db.relationship('Questions',backref='grades',cascade='all, delete')
    interviewer_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    interviewer = db.relationship('User',backref='grades',cascade='all, delete')
    interview_id = db.Column(db.Integer,db.ForeignKey('interview.id'))
    interview = db.relationship('Interview',backref='grades',cascade='all, delete')
    grade = db.Column(db.Integer)

    def __repr__(self):

        return f'{self.interviewer} rated question \"{self.question}\" {self.grade}'

class Category(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    def __repr__(self):

        return self.name


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Interview, db.session))
admin.add_view(ModelView(Questions, db.session))
admin.add_view(ModelView(Category, db.session))