#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Create the directory for static files if it doesn't exist
mkdir -p staticfiles_build

# Move the collected static files to the staticfiles_build directory
cp -r staticfiles/* staticfiles_build/
