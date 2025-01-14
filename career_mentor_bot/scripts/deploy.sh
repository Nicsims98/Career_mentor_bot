#!/bin/bash

# Deployment script for Sage Career Mentor

ENV=$1
if [ -z "$ENV" ]; then
    echo "Usage: ./deploy.sh [development|staging|production]"
    exit 1
fi

# Load environment variables
set -a
source .env.$ENV
set +a

# Install dependencies
echo "Installing dependencies..."
python -m pip install -r requirements.txt

# Run database migrations
echo "Running database migrations..."
flask db upgrade

# Run tests if not production
if [ "$ENV" != "production" ]; then
    echo "Running tests..."
    pytest
fi

# Start the application
echo "Starting application in $ENV mode..."
if [ "$ENV" = "production" ]; then
    gunicorn -w 4 -b 0.0.0.0:$PORT "src.app:create_app()"
else
    flask run --host=0.0.0.0 --port=$PORT
fi
