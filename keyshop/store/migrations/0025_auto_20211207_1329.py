# Generated by Django 3.2.9 on 2021-12-07 11:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0024_auto_20211207_1320'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category_for_product', to='store.category')),
                ('products', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_for_category', to='store.product')),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='category_product',
            field=models.ManyToManyField(related_name='product_for_that_category', to='store.CategoryProduct'),
        ),
    ]
