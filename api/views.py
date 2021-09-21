import logging

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from api import models, tasks, utils, serializers

logger = logging.getLogger(__name__)

# Create your views here.
@csrf_exempt
@api_view(['POST'])
def execute(request, command_id):
    try:
        command = models.Command.objects.get(pk=command_id)
        machines = request.data.get('machines', [])
        command_options = request.data.get('command_options', '')
        params =  request.data.get('parameters', '')
        full_command = utils.generate_full_command(command, command_options, params)
        results = []

        requires_input = command.requires_input

        for machine_dict in machines:
            machine = models.Machine.objects.get(pk=machine_dict.pop('machine_id'))
            result = models.Result(
                user=request.user, machine=machine, executed_command=full_command)
            result.save()
            results.append(result)
            machine_dict['ip_address'] = machine.ip_address
            tasks.ssh_remote_machine.delay(machine_dict, requires_input,
                                            full_command, result.result_id)
        serialized = serializers.ResultSerializer(results, many=True)
        return Response(serialized.data, status=status.HTTP_202_ACCEPTED)
    except Exception as e:
        logger.exception(e)
    message = {
        'error': 'An error occurred while attemtping to execute command on remote host.'
    }
    return Response(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)