import asyncio

# from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from asgiref.sync import async_to_sync
from rest_framework.decorators import api_view
from rest_framework.response import Response
from paramiko.client import AutoAddPolicy, SSHClient

from api.models import Command, CommandOptions

def generate_full_command(command_id, command_options):
    cmd = ''
    command = Command.objects.get(pk=command_id)
    cmd = f'{command.command_name}'
    for option in command_options:
        co = CommandOptions.objects.get(pk=option)
        cmd = f'{cmd} -{co.option} '
    print(f'full command: {cmd}')
    return cmd

# async def ssh_remote_machine(request):
def ssh_remote_machine(data, command_id):
    # import pdb; pdb.set_trace()
    client = SSHClient()
    try:
        client.set_missing_host_key_policy(AutoAddPolicy())
        machines = data.pop('machines')
        cmd_options = data.pop('cmd_options')
        full_command = generate_full_command(command_id, cmd_options)
        client.connect(**data)
        stdin, stdout, stderr = client.exec_command(full_command)
        # commands that require input e.g. when sudo asks for a password
        # stdin.write(request.data['password'])
        lines = stdout.readlines()
        print('printing stdout')
        for i in lines:
            print(i)
        lines = stderr.readlines()
        print('printing stderr')
        for i in lines:
            print(i)
    except Exception as e:
        print('An error occurred while attemtping to execute command on remote host.')
        print(e)
    finally:
        client.close()
        print('connection successfully closed.')

# Create your views here.
@csrf_exempt
@api_view(['GET', 'POST'])
def execute(request, command_id):
    if request.method == 'POST':
        # loop = asyncio.get_event_loop()
        # loop.create_task(ssh_remote_machine(request.data))
        # async_to_sync(ssh_remote_machine(request.data))
        ssh_remote_machine(request.data, command_id)
        return Response({'message': 'command has been sent to remote host.'})
    return Response({'error': f'Method {request.method} not allowed'})