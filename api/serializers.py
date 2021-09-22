from django.contrib.auth.models import User
from rest_framework import serializers

from api import models

class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Machine
        fields = ('machine_id', 'ip_address', 'hostname')


class CommandOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CommandOptions
        fields = ('option_id', 'option', 'description')


class CommandSerializer(serializers.ModelSerializer):
    commandoption = CommandOptionsSerializer(many=True, read_only=True)
    class Meta:
        model = models.Command
        fields = ('command_id', 'command_name', 'requires_input',
                    'commandoption',)


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Result
        fields = ('result_id', 'created_at', 'executed_command',
                    'std_out', 'std_err', 'user', 'machine', 'status')
        read_only_fields = ('result_id', 'created_at', 'executed_command',
                    'std_out', 'std_err', 'user', 'machine', 'status')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class MachineDataSerializer(serializers.Serializer):
    machine_id = serializers.IntegerField(required=True)
    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=100, required=True)


class ExecuteCommandSerializer(serializers.Serializer):
    machines = MachineDataSerializer(many=True, required=True)
    command_options = serializers.ListField(
        child=serializers.CharField(max_length=10),
        required=False
    )
    parameters = serializers.ListField(
        child=serializers.CharField(max_length=50),
        required=False
    )