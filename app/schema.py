from marshmallow import fields, validate

from app.models import *
from app import ma,db

class UserSchema(ma.SQLAlchemyAutoSchema):

	class Meta:
		model = User
		include_relationship = True
		load_instance = True
		exclude = ['private_key','password_hash','id','role']

	id = ma.auto_field()

class InterviewSchema(ma.SQLAlchemyAutoSchema):

	class Meta:
		model = Interview
		include_relationship = True
		load_instance = True

	id = ma.auto_field()
	recrutier = fields.Nested("UserSchema")
	question = fields.Nested("QuestionSchema",many=True)
	interviewer = fields.Nested("UserSchema",many=True)
	grades = fields.Nested('GradeSchema',many=True)

class QuestionSchema(ma.SQLAlchemyAutoSchema):

	class Meta:
		model = Questions
		include_relationship = True
		load_instance = True

	id = ma.auto_field()

class GradeSchema(ma.SQLAlchemyAutoSchema):

	class Meta:
		model = Grades
		include_relationship = True
		load_instance = True
		exclude = ['id']

	question = fields.Nested('QuestionSchema',exclude=['grade'])