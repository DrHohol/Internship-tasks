from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, SelectMultipleField, IntegerField
from wtforms.validators import DataRequired, NumberRange

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    sumbit = SubmitField('Sign in')

class InterviewCreationForm(FlaskForm):

    interview_title = StringField('Interview name',validators=[DataRequired()])
    candidat_name = StringField('Candidat name',validators=[DataRequired()])
    recrutier = SelectField('recrutier',choices=[],validators=[DataRequired()])
    experts = SelectMultipleField('experts',choices=[],validators=[DataRequired()],coerce=int)
    questions = SelectMultipleField('questions',choices=[],validators=[DataRequired()],coerce=int)
    zoom = StringField('zoom')
    
    create = SubmitField('Create')

class QuestionCreateForm(FlaskForm):

    question = StringField('Question',validators=[DataRequired()])

    max_grade = IntegerField('Maximum grade', validators=[NumberRange(min=1),DataRequired()])
    category = SelectMultipleField('Category',choices=[],coerce=int)

    create = SubmitField('Create')