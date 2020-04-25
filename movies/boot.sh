#!/bin/sh

echo "Waiting for MySQL..."
sleep 60
echo "Resume..."


source venv/bin/activate
flask initdb
# flask translate compile
exec gunicorn -b :5000 --access-logfile - --error-logfile - movies:application