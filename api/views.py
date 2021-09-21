import asyncio
import logging

# from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from asgiref.sync import async_to_sync
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from paramiko.client import AutoAddPolicy, SSHClient

from api.models import Command, CommandOptions, Result, Machine
from api import serializers

logger = logging.getLogger(__name__)

def generate_full_command(command_id, command_options, params):
    cmd = ''
    command = Command.objects.get(pk=command_id)
    cmd = f'{command.command_name}'
    for option in command_options:
        co = CommandOptions.objects.get(pk=option)
        if co.command.command_id == command.command_id:
            # only add the option if it belongs to command
            cmd = f'{cmd} -{co.option} '
    for param in params:
        cmd = f'{cmd} {param} '
    logger.info(f'full command: {cmd}.')
    return cmd

# async def ssh_remote_machine(request):
def ssh_remote_machine(user, data, command_id):
    results = []
    client = SSHClient()
    try:
        client.set_missing_host_key_policy(AutoAddPolicy())
        # construct the command that will be executed
        cmd_options = data.pop('cmd_options')
        params = data.get('parameters', [])
        full_command = generate_full_command(command_id, cmd_options, params)
        # execute command for each machine_id supplied
        machines = data.pop('machines')
        for machine_dict in machines:
            machine = Machine.objects.get(pk=machine_dict['machine_id'])
            client.connect(
                username=machine_dict['username'],
                password=machine_dict['password'],
                hostname=machine.ip_address
            )
            stdin, stdout, stderr = client.exec_command(full_command)
            # commands that require input e.g. when sudo asks for a password
            # stdin.write(request.data['password'])
            result = Result(executed_command=full_command,
                                user=user, machine=machine)
            # store stdout
            stored = ''
            lines = stdout.readlines()
            for i in lines:
                stored += i + '\n'
            result.std_out = stored
            # store stderr
            stored = ''
            lines = stderr.readlines()
            for i in lines:
                stored += i + '\n'
            result.std_err = stored
            result.save()
            results.append(result)
            client.close()
        logger.info('stdout and/or stderr successfully stored in database.')
    except Exception as e:
        logger.info('An error occurred while attemtping to execute command on remote host.')
        logger.exception(e)
    finally:
        client.close()
        logger.info('client connection successfully closed.')
    return results

# Create your views here.
@csrf_exempt
@api_view(['GET', 'POST'])
def execute(request, command_id):
    """
    JSON payload strucure:
    
        {
            "cmd_options": [<command_option_id_1>, <command_option_id_2>,...],
            "machines": [
                {
                    "machine_id": <machine_id>,
                    "username": "<username>",
                    "password": "<password>"
                },
                ...
            ],
            "parameters": [<parameter_1>, <parameter_2>,...]
        }
    """
    if request.method == 'POST':
        # loop = asyncio.get_event_loop()
        # loop.create_task(ssh_remote_machine(request.data))
        # async_to_sync(ssh_remote_machine(request.data))
        result = ssh_remote_machine(request.user, request.data, command_id)
        if result:
            serializer = serializers.ResultSerializer(result, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        message = {
            'error': 'Could not successfully execute command on remote host.'
        }
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    message = {'error': f'Method {request.method} not allowed'}
    return Response(message, status=status.HTTP_405_METHOD_NOT_ALLOWED)