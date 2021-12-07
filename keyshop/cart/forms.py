from django import forms
from store.models import Product

PRODUCT_QUANTITY_CHOICES = [(i,str(1)) for i in range(1,10)]

class CartAddProductForm(forms.Form):

	quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,coerce=int)
	override = forms.BooleanField(required=False,initial=False,widget=forms.HiddenInput)