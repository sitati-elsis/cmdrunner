from rest_framework import serializers

from api import models

class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Machine
        fields = ('ip_address', 'hostname')