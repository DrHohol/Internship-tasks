from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
#admin.site.register(Wishlist)
admin.site.register(Customer)


@admin.register(KeyInstance)
class KeyInstanceAdmin(admin.ModelAdmin):
	list_display = ('product','key_id')