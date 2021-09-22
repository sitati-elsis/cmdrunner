import time
import logging

from celery import shared_task
from paramiko.client import AutoAddPolicy, SSHClient

from api import models


logger = logging.getLogger(__name__)

@shared_task
def ssh_remote_machine(machine, requires_input, full_command, result_id):
    client = SSHClient()
    try:
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(
            username=machine['username'],
            password=machine['password'],
            hostname=machine['ip_address'],
            timeout=10,
        )
        stdin, stdout, stderr = client.exec_command(full_command, timeout=10)
        # commands that require input e.g. when sudo asks for a password
        if requires_input:
            command_input = data['command_input']
            stdin.write(command_input + '\n')
            stdin.flush()
        result = models.Result.objects.get(pk=result_id)
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
        result.status = 'COMP'
        result.save()
        client.close()
        logger.info('stdout and/or stderr successfully stored in database.')
    except Exception as e:
        logger.info('An error occurred while attemtping to execute command on remote host.')
        logger.exception(e)
    finally:
        client.close()
        logger.info('client connection successfully closed.')