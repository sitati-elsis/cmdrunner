# Generated by Django 3.2.7 on 2021-09-16 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_command_parameters'),
    ]

    operations = [
        migrations.AddField(
            model_name='commandoptions',
            name='description',
            field=models.CharField(default='Description', max_length=100),
            preserve_default=False,
        ),
    ]