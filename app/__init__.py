from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_login import LoginManager, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_restful import Api, Resource, reqparse
import secrets

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
login = LoginManager(app)
login.login_view = 'login'
admin = Admin(app,name='Admin Panel')
api = Api(app)
ma = Marshmallow(app)

from app import routes, models, api_routes
db.create_all()

root_user = models.User.query.filter_by(role=0).first()
if not root_user:
	root_user = models.User(username='admin',role=0,private_key=secrets.token_urlsafe(16))
	db.session.add(root_user)
	root_user.set_password('password')
	db.session.commit()


class AdminModelView(ModelView):

    def is_accessible(self):
        if current_user.is_authenticated:
        	if current_user.role == 0:
        		return True
        return current_user.is_authenticated

admin.add_view(AdminModelView(models.User, db.session,name='Users'))
admin.add_view(AdminModelView(models.Interview, db.session, name='Interviews'))
admin.add_view(AdminModelView(models.Questions, db.session))
admin.add_view(AdminModelView(models.Category,db.session,name='Catergories'))

api.add_resource(api_routes.UserApi,'/api/user')
api.add_resource(api_routes.SetPasswordApi,'/api/set-password')
api.add_resource(api_routes.GetInterviewsApi,'/api/interviews')
api.add_resource(api_routes.CreateInterviewApi,'/api/create-interview')
api.add_resource(api_routes.GetInterviewInfoApi,'/api/interview-info')
api.add_resource(api_routes.GradeAnswerApi,'/api/grade')
api.add_resource(api_routes.QuestionApi,'/api/questions')
