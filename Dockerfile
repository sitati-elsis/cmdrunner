FROM python:3.9

RUN mkdir /code

WORKDIR /code

COPY . /code/

RUN pip install pipenv

RUN pipenv install --system

RUN mkdir -p /var/log/django/

EXPOSE 7331

# pg_ready command is installed through this package.
# The command will be used to poll the "db" container to check if postgres is
# ready to accept connections. When ready, migrations will be run in the
# entrypoint script.
RUN apt-get update && apt-get install -f -y postgresql-client

RUN chown root:root /code/docker_entrypoint.sh && chmod 755 /code/docker_entrypoint.sh

ENTRYPOINT /code/docker_entrypoint.sh