# Generated by Django 3.2 on 2021-06-18 11:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Tester', '0003_result_totalmarks'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='userEmail',
            field=models.ForeignKey(default=' ', on_delete=django.db.models.deletion.CASCADE, to='Tester.user'),
            preserve_default=False,
        ),
    ]
