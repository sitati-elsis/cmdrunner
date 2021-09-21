from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Machine(models.Model):
    machine_id = models.IntegerField(primary_key=True)
    ip_address = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    hostname = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.ip_address}'

class Command(models.Model):
    command_id = models.IntegerField(primary_key=True)
    command_name = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.command_name}'

class CommandOptions(models.Model):
    option_id = models.IntegerField(primary_key=True)
    option = models.CharField(max_length=15)
    description = models.CharField(max_length=100)
    command = models.ForeignKey(Command, on_delete=models.CASCADE, related_name='commandoption')

    def __str__(self):
        return f'{self.command.command_name} {self.option}'

class Result(models.Model):
    result_id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    executed_command = models.CharField(max_length=255)
    std_out = models.TextField()
    std_err = models.TextField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='result')

    def __str__(self):
        return f'{self.result_id}'