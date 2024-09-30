#!/bin/sh

# Wait for PostgreSQL to be available
echo "Waiting for PostgreSQL..."
python wait_for_postgres.py

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Create superuser if it does not exist
echo "Creating superuser if it does not exist..."
python manage.py create_superuser

# Populate initial data if POPULATE_DATA is set to True
if [ "$POPULATE_DATA" = "True" ]; then
    echo "Populating initial data..."
    python manage.py populate_initial_data
fi

# Start the server
echo "Starting server..."
python manage.py runserver 0.0.0.0:8000

# Delete initial data on shutdown (trap SIGTERM and SIGINT)
trap 'echo "Deleting initial data..."; python manage.py delete_initial_data' SIGTERM SIGINT

# Keep the script running to catch signals
tail -f /dev/null

