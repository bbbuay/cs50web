# Generated by Django 4.1.3 on 2022-12-09 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_user_follower_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]