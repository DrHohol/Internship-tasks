# Generated by Django 3.2.9 on 2021-12-07 07:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_auto_20211207_0921'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='slug',
        ),
    ]