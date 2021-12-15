from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


question_indef = db.Table('question_indentif',
	db.Column('question_id',db.Integer,db.ForeignKey('questions.id')),
	db.Column('interview_id',db.Integer,db.ForeignKey('interview.id')))


class User(db.Model):
	'''Table for user'''
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(64),index=True,unique=True)
	role = db.Column(db.Integer)
	password_hash = db.Column(db.String(256))

	def __repr__(self):

		return '<User {}>'.format(self.username)

class Interview(db.Model):

	id = db.Column(db.Integer,primary_key=True)
	title = db.Column(db.String(64))
	description = db.Column(db.String(255))
	interviewer = db.Column(db.String(64), db.ForeignKey('user.username'))
	recrutier = db.Column(db.String(64),db.ForeignKey('user.username'))
	candidat = db.Column(db.String(64),db.ForeignKey('user.username'))
	question = db.relationship('Questions',backref='interview',lazy=True,secondary=question_indef)
	candidat_answer = db.Column(db.String(128))
	final_grade = db.Column(db.Integer) 

	def __repr__(self):

		return '<Interview {} with {}>'.format(self.title,self.candidat)

class Questions(db.Model):

	id = db.Column(db.Integer,primary_key=True)
	question = db.Column(db.String(128))
	answer = db.Column(db.String(255))
	grade = db.Column(db.Integer)
	max_grade = db.Column(db.Integer)

	def __repr__(self):

		return '<question: >'.format(self.question)


class Category(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64))