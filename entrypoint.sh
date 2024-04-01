#!/bin/sh
# Export environment variables
export FLASK_APP=app.py
export FLASK_ENV=development


# Wait for the database to be ready
echo "Waiting for database..."
while ! nc -z db 3306; do
    sleep 1
done

# Run database migrations
flask db upgrade

# Execute the main command (CMD in Dockerfile)
exec "$@"
