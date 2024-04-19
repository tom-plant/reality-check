#!/bin/sh
export FLASK_APP=backend/app.py
export FLASK_ENV=development

echo "Waiting for database..."
while ! nc -z db 3306; do
    sleep 1
done

flask db upgrade
exec "$@"