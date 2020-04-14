#!/bin/bash

echo "=============================================================================="
echo "GENERATING MIGRATIONS" 
echo "=============================================================================="

python3 /home/atcs/django_museum/manage.py makemigrations

echo "=============================================================================="
echo "MIGRATING" 
echo "=============================================================================="

python3 /home/atcs/django_museum/manage.py migrate