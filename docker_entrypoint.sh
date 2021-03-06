set -e

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# set ownership for log files
mkdir -p $HOME/log/celery/ && chown celery:celery $HOME/log/celery/
# start celery worker
celery -A cmdrunner multi start worker1 \
    --pidfile="$HOME/run/celery/%n.pid" \
    --logfile="$HOME/log/celery/%n%I.log"

# Start server
echo "Starting server"
gunicorn cmdrunner.asgi:application -b 0.0.0.0:7331 -k uvicorn.workers.UvicornWorker