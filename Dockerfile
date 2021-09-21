FROM python:3.9

RUN mkdir /code

WORKDIR /code

COPY . /code/

RUN pip install pipenv

RUN pipenv install --system

ENV DJANGO_SETTINGS_MODULE="cmdrunner.settings.prod_settings"

# secure this.
ENV SECRET_KEY='SECURE THIS KEY'

RUN mkdir -p /var/log/django/

RUN python manage.py makemigrations && \
        python manage.py migrate

EXPOSE 7331

CMD ["gunicorn", "cmdrunner.asgi:application",\
        "-b 0.0.0.0:7331", "-k uvicorn.workers.UvicornWorker"]