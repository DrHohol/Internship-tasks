# Generated by Django 3.2.9 on 2021-12-07 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_rename_customer_customer_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='InStock',
            field=models.PositiveBigIntegerField(default=1),
        ),
    ]
