from django.urls import path, re_path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.BaseView.as_view(), name='index'),
    path('catalog/', views.Products.as_view(),name='products'),
    re_path(r'^key/(?P<pk>\d+)$', views.ProductDetail.as_view(), name='product'),
    path('wishlist/',views.Wishlist.as_view(),name='wishlist'),
    path('wishlist-add/<int:product_id>/',views.AddToWishlist.as_view(),name='add_wishlist'),
    path('category/<str:Category_slug>/', views.Categories.as_view(),name='category'),
    path('wishlist-remove/<int:product_id>/',views.RemoveFromWishlist.as_view(),name="remove_wishlist")

]
