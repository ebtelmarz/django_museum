# Generated by Django 3.0.5 on 2020-04-10 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museum', '0002_auto_20200410_2014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='date',
            field=models.CharField(max_length=50),
        ),
    ]
