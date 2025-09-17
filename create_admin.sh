#!/bin/bash

# Script to create admin superuser for ALX Project Nexus
# This script can be run during deployment or manually

echo "Creating admin superuser for ALX Project Nexus..."

# Run the Django management command to create superuser
python manage.py createsuperuser --username wuor --password 1234 --email admin@alx-project-nexus.com --force

echo "Superuser creation completed!"
echo "You can now login to the admin panel with:"
echo "Username: wuor"
echo "Password: 1234"
echo "Admin URL: /admin/"
