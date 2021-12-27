from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_login import LoginManager
from flask_admin import Admin
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
login = LoginManager(app)
login.login_view = 'login'
admin = Admin(app)
api = Api(app)
ma = Marshmallow(app)

from app import routes, models, api_routes

api.add_resource(api_routes.UserCreateApi,'/api/create-user')
api.add_resource(api_routes.SetPasswordApi,'/api/set-password')
api.add_resource(api_routes.GetInterviewsApi,'/api/interviews')
api.add_resource(api_routes.CreateInterviewApi,'/api/create-interview')
api.add_resource(api_routes.GetInterviewInfoApi,'/api/interview-info')