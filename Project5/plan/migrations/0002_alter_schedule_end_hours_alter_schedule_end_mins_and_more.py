# Generated by Django 4.1.3 on 2022-12-19 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='end_hours',
            field=models.CharField(max_length=2),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='end_mins',
            field=models.CharField(max_length=2),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='start_hours',
            field=models.CharField(max_length=2),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='start_mins',
            field=models.CharField(max_length=2),
        ),
    ]