from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from store.models import Product
from .forms import CartAddProductForm
from django.views.decorators.http import require_POST

# Create your views here.

@require_POST
def cart_add(request,product_id):

	cart = Cart(request)
	product = get_object_or_404(Product, id=product_id)
	form = CartAddProductForm(request.POST)

	if form.is_valid():
		cd = form.cleaned_data
		cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
	else:
		print(form)

	return redirect('cart_detail')

@require_POST
def cart_remove(request,product_id):

	cart = Cart(request)
	product = get_object_or_404(Product, id=product_id)
	cart.remove(product=product)
	return redirect('cart_detail')

def cart_detail(request):
	
	cart = Cart(request)
	cart_product_form = CartAddProductForm()
	return render(request,'cart/detail.html',{'cart':cart})