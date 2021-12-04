from django.contrib import admin
from .models import Product, KeyInstance, Category

# Register your models here.

admin.site.register(Category)
admin.site.register(Product)

@admin.register(KeyInstance)
class KeyInstanceAdmin(admin.ModelAdmin):
	list_display = ('product','key_id')