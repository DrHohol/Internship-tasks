from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.BaseView.as_view(), name='index'),
    url(r'^catalog/$', views.Products.as_view(),name='products'),
    url(r'^key/(?P<pk>\d+)$', views.ProductDetail.as_view(), name='product'),
    url(r'^wishlist/$',views.Wishlist.as_view(),name='wishlist'),
    path('<str:Category_slug>/', views.Categories.as_view(),name='categories'),
    
]
