from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^register/$', views.Register,name='register'),
]