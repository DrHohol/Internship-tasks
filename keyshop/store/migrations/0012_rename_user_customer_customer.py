# Generated by Django 3.2.9 on 2021-12-06 08:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_category_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='user',
            new_name='customer',
        ),
    ]