from django.shortcuts import render
from .models import *
from django.views import generic, View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django import forms


# Create your views here.

class BaseView(View):
    """docstring for BaseView"""
    category = Category.objects.all()
    def get(self,request,*args,**kwargs):
        return render(request,'index.html',{})
        

def index(request):

    model = Product
    category = Categories.objects.all
    context = {'category':Category}
    return render(request,'index.html')


class Products(generic.ListView):
    model = Product
    paginate_by = 6


class ProductDetail(generic.DetailView):

    model = Product


class Categories(generic.DetailView):

    model = Category
    slug_url_kwarg = 'Category_slug'
    context_object_name = 'category'
    template_name = 'store/category.html'


class Wishlist(View):

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        context = {
            'customer': customer
        }
        return render(request, 'store/customer_list.html', context)



    '''
    def get(self,request,*args,**kwargs):
        customer = Customer.objects.get(user=request.user)
        context_object_name = 'customer'

        return render(request,"store/customer_list.html")
    '''
#    model = Customer
#    template_name = '/templates/wislist_list.html'



'''
    def get_customer(self):

        return Wishlist.objects.filter(customer=self.request.user)

'''        
'''
    def get_wishlist(self):

        return Wishlist.objects.all.filter(Owner = self.get_customer(self.request))
'''