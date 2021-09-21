from rest_framework import serializers

from api import models

class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Machine
        fields = ('ip_address', 'hostname')


class CommandOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CommandOptions
        fields = ('option_id', 'option', 'description')


class CommandSerializer(serializers.ModelSerializer):
    commandoption = CommandOptionsSerializer(many=True, read_only=True)
    class Meta:
        model = models.Command
        fields = ('command_name', 'commandoption')


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Result
        fields = ('result_id', 'created_at', 'executed_command',
                    'std_out', 'std_err', 'user')
        read_only_fields = ('result_id', 'created_at', 'executed_command',
                    'std_out', 'std_err', 'user')
