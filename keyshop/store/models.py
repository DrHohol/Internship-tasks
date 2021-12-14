from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
import uuid
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.text import slugify

class Category(models.Model):

    name = models.CharField(max_length=255,help_text='Enter name of category: game, software, antivirus, etc')
    #products = models.ManyToManyField('CategoryProduct',related_name='product_for_that_category')
    slug = models.SlugField(null=True)

    def __str__(self):

        return self.name

    def get_absolute_url(self):
 
        return reverse('category', kwargs={'Category_slug':self.slug})


class Product(models.Model):

    title = models.CharField('Title',max_length=255)
    image = models.ImageField(upload_to='product_picture')
    category = models.ManyToManyField(Category,max_length=255,help_text='Select product category ')
    description = models.CharField('Description',max_length=255,help_text='Enter desctiption of the product')
    availability = (
        ('a','availabile'),
        ('n','not available'))
    status = models.CharField(max_length=1, choices=availability, blank=True, default='a', help_text='Key availability')
    price = models.FloatField(help_text='Product price',default=0)
    InStock = models.PositiveSmallIntegerField(default=1)

    def __str__(self):

        return self.title

    def get_absolute_url(self):
        """
        Returns the url to access a product
        """
        return reverse('product', args=[str(self.id)])
'''
class CategoryProduct(models.Model):

    product = models.ForeignKey(Product ,on_delete=models.CASCADE,null=True,related_name='product_for_category')
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True,related_name='category_for_product')

    def __str__(self):

        return f"Product {self.product.title} associate with {self.category.name}"
'''


class KeyInstance(models.Model):

    key_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    
    value = models.CharField(max_length=255,help_text="Key value")

    def __str__(self):
        
        return '%s %s %s' % (self.key_id,self.product.title,self.value)

class Customer(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    wishlist = models.ManyToManyField(Product)

    def __str__(self):
        
        return f"{self.user.username}"



