# Generated by Django 3.2.7 on 2021-09-21 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_commandoptions_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='executed_command',
            field=models.CharField(default='ls -l', max_length=255),
            preserve_default=False,
        ),
    ]