# Generated by Django 3.0.5 on 2020-04-10 20:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('museum', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='position_x',
        ),
        migrations.RemoveField(
            model_name='location',
            name='position_y',
        ),
    ]