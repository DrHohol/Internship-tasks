from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_login import LoginManager
from flask_admin import Admin
from flask_restful import Api, Resource, reqparse
import secrets

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
db.create_all()
migrate = Migrate(app,db)
login = LoginManager(app)
login.login_view = 'login'
admin = Admin(app)
api = Api(app)
ma = Marshmallow(app)

from app import routes, models, api_routes

admin = models.User.query.filter_by(role=0).first()
if not admin:
	admin = User(username=admin,role=0,private_key=secrets.token_urlsafe(16))
	admin.set_password('password')

api.add_resource(api_routes.UserCreateApi,'/api/create-user')
api.add_resource(api_routes.SetPasswordApi,'/api/set-password')
api.add_resource(api_routes.GetInterviewsApi,'/api/interviews')
api.add_resource(api_routes.CreateInterviewApi,'/api/create-interview')
api.add_resource(api_routes.GetInterviewInfoApi,'/api/interview-info')
api.add_resource(api_routes.GradeAnswerApi,'/api/grade')
api.add_resource(api_routes.CreateQuestionApi,'/api/create-question')