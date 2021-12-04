from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
import uuid

class Category(models.Model):

    name = models.CharField(max_length=255,help_text='Enter name of category: game, software, antivirus, etc')

    def __str__(self):

        return self.name

    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('category', args=[str(self.id)])

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

    def __str__(self):

        return self.title

    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('product', args=[str(self.id)])

    def display_category(self):

        return ','.join([category.name for category in self.category.all()[:3]])

    display_category.short_description = 'Category'

class KeyInstance(models.Model):
    key_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    
    value = models.CharField(max_length=255,help_text="Key value")

    def __str__(self):
        
        return '%s %s %s' % (self.key_id,self.product.title,self.value)