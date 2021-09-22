import logging

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework import status

from api import models, tasks, utils, serializers

logger = logging.getLogger(__name__)

# Create your views here.
class ExecuteCommand(CreateAPIView):
    serializer_class = serializers.ExecuteCommandSerializer

    def post(self, request, command_id):
        """
        create:
            Create a new machine.
        """
        try:
            serializer = serializers.ExecuteCommandSerializer(data=request.data)
            if serializer.is_valid():
                command = models.Command.objects.get(pk=command_id)
                machines = request.data.get('machines', [])
                command_options = request.data.get('command_options', '')
                params =  request.data.get('parameters', '')
                full_command = utils.generate_full_command(
                    command, command_options, params)
                results = []

                requires_input = command.requires_input

                # check validity of machine data
                for machine_dict in machines:
                    mds_serializer = serializers.MachineDataSerializer(
                                                        data=machine_dict)
                    if not mds_serializer.is_valid():
                        return Response(
                                mds_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)

                for machine_dict in machines:
                    machine = models.Machine.objects.get(
                                        pk=machine_dict.pop('machine_id'))
                    result = models.Result(
                                user=request.user, machine=machine,
                                executed_command=full_command)
                    result.save()
                    results.append(result)
                    machine_dict['ip_address'] = machine.ip_address
                    tasks.ssh_remote_machine.delay(
                        machine_dict, requires_input,
                        full_command, result.result_id
                    )
                res_serializer = serializers.ResultSerializer(results, many=True)
                return Response(res_serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(e)
        message = {
            'error': 'An error occurred while attemtping to execute command on remote host.'
        }
        return Response(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)