# Generated by Django 3.2.7 on 2021-09-21 09:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_result_executed_command'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='std_in',
        ),
    ]