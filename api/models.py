from django.db import models

# Create your models here.
class Machine(models.Model):
    machine_id = models.IntegerField(primary_key=True)
    ip_address = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    hostname = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.ip_address}'