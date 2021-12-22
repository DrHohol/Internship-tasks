from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, SelectMultipleField, IntegerField
from wtforms.validators import DataRequired, NumberRange, EqualTo, ValidationError
from app.models import User

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

class GradeInterviewForm(FlaskForm):

    def __init__(self,max_grade):
        super().__init__(*args, **kwargs)
        max_grade=self.max_grade
        self.gradeform = self.GradeForm()

    def GradeForm(self):
        grade = IntegerField('Grade',validators=[NumberRange(max=self.max_grade)])

class CreateUserForm(FlaskForm):
    '''Form for create new user (only for admin)'''
    username = StringField('Username',validators=[DataRequired()])
    firstname = StringField('First Name',validators=[DataRequired()])
    lastname = StringField('Last Name',validators=[DataRequired()])
    role = SelectField('recrutier',choices=[(1,'interviewer'),(2,'expert')],validators=[DataRequired()],coerce=int)

    create = SubmitField('Create')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

class SetPasswordForm(FlaskForm):
    '''Setting for new user by himself'''
    password = PasswordField('Password',validators=[DataRequired()])
    password_check = PasswordField(
        'Repeat password',validators=[DataRequired(),EqualTo('password')])

    sumbit = SubmitField('Sumbit')

