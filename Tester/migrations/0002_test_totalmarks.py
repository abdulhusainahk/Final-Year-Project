# Generated by Django 3.2 on 2021-06-18 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tester', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='totalMarks',
            field=models.IntegerField(default=0),
        ),
    ]
