FROM python:alpine3.14

RUN mkdir /code

WORKDIR /code

COPY . /code/

COPY celery_prod/celeryd.conf /etc/default/
COPY celery_prod/celeryd /etc/init.d/celeryd

RUN mv /etc/default/celeryd.conf /etc/default/celeryd && \
    chmod 755 /etc/default/celeryd && \
    chmod 755 /etc/init.d/celeryd

# create celery user and disable login
RUN adduser --disabled-password celery && \
    addgroup celery celery

RUN apk add --no-cache libffi-dev make python3-dev automake g++ \
    autoconf postgresql-dev musl-dev
# RUN apk add --no-cache libffi-dev make python3-dev gcc

RUN pip install pipenv

RUN pipenv install --system

RUN mkdir -p /var/log/django/

EXPOSE 7331

# pg_ready command is installed through this package.
# The command will be used to poll the "db" container to check if postgres is
# ready to accept connections. When ready, migrations will be run in the
# entrypoint script.
RUN apk add postgresql-client

RUN chown root:root /code/docker_entrypoint.sh && chmod 755 /code/docker_entrypoint.sh

ENTRYPOINT /code/docker_entrypoint.sh