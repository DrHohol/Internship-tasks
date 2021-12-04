from django.shortcuts import render
from .models import *
from django.views import generic

# Create your views here.

def index(request):
	model = Product
	return render(request,'index.html')

class Products(generic.ListView):
	model = Product
	paginate_by = 6

class ProductDetail(generic.DetailView):
	model = Product

class Categories(generic.ListView):
	model = Category