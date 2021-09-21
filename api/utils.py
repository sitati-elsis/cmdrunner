import logging

logger = logging.getLogger(__name__)

def generate_full_command(command, command_options, params):
    cmd = ''
    cmd = f'{command.command_name}'
    for option in command_options:
        # fetching this directly using .get(pk=option) will get a DoesNotExist
        # if the pk does not exist in the DB
        co = CommandOptions.objects.filter(pk=option, command=command)
        if len(co) == 1:
            co = co[0]
            cmd = f'{cmd} -{co.option} '
    for param in params:
        cmd = f'{cmd} {param} '
    logger.info(f'full command: {cmd}.')
    return cmd