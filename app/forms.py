from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, SelectMultipleField, IntegerField, DateField, TimeField
from wtforms.validators import DataRequired, NumberRange, EqualTo, ValidationError
from app.models import User, Questions

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
    date = DateField('Date of interview')
    time = TimeField('Time of interview')
    create = SubmitField('Create')

class QuestionCreateForm(FlaskForm):

    question = StringField('Question',validators=[DataRequired()])

    max_grade = IntegerField('Maximum grade', validators=[NumberRange(min=1),DataRequired()])
    category = SelectMultipleField('Category',choices=[],coerce=int)

    create = SubmitField('Create')

class GradeInterviewForm(FlaskForm):

    ''' Validate max grade for each question'''
    def max_grade(question,grade):

        max_grade = Questions.query.filter_by(id=question.data.get('question')).first().max_grade
        if grade.data > max_grade:
            raise ValidationError('Grade is bigger than maximum for this question')

    question = SelectField('question',choices=[], validators=[DataRequired()])
    grade = IntegerField('grade',validators=[DataRequired(),NumberRange(min=0),max_grade])
    sumbit = SubmitField('Sumbit')


'''
    def __init__(self,questions):
        super().__init__(*args, **kwargs)
        max_grade=self.max_grade
        self.gradeform = self.GradeForm()
       # def GradeForm(self):
 '''

class CreateUserForm(FlaskForm):
    '''Form for create new user (only for admin)'''
    username = StringField('Username',validators=[DataRequired()])
    firstname = StringField('First Name',validators=[DataRequired()])
    lastname = StringField('Last Name',validators=[DataRequired()])
    role = SelectField('recrutier',choices=[(2,'recrutier'),(1,'expert')],validators=[DataRequired()],coerce=int)

    create = SubmitField('Create')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

class SetPasswordForm(FlaskForm):
    '''Setting password for new user by himself'''
    password = PasswordField('Password',validators=[DataRequired()])
    password_check = PasswordField(
        'Repeat password',validators=[DataRequired(),EqualTo('password')])

    sumbit = SubmitField('Sumbit')

class CreateCategoryForm(FlaskForm):
    '''Create new category'''

    category_name = StringField('Category name',validators=[DataRequired()])
    create = SubmitField('Create')

class EditQuestionForm(FlaskForm):
    '''edit or delete question'''
    question = SelectField('Question',choices=[],validators=[DataRequired()],coerce=int)

    new_text = StringField('Text',validators=[DataRequired()])
    new_max = IntegerField('New maximum grade',validators=[DataRequired()])
    sumbit = SubmitField('Sumbit')