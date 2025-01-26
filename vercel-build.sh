#!/bin/bash

# Run any necessary build steps
echo "Running build steps..."

# Install dependencies
pip install -r requirements.txt

# Collect static files (if using Django)
python manage.py collectstatic --noinput
