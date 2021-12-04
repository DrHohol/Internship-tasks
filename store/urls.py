from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^catalog/$', views.Products.as_view(),name='products'),
    url(r'^key/(?P<pk>\d+)$', views.ProductDetail.as_view(), name='product'),
    url(r'^category/$', views.Categories.as_view(),name='categories'),
]
