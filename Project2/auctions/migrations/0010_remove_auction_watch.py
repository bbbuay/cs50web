# Generated by Django 4.1.3 on 2022-11-24 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_category_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auction',
            name='watch',
        ),
    ]
