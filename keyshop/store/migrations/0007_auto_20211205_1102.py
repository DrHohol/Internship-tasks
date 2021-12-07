# Generated by Django 3.2.9 on 2021-12-05 09:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_auto_20211205_1038'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='Products',
        ),
        migrations.AddField(
            model_name='wishlist',
            name='Products',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.product'),
        ),
    ]
