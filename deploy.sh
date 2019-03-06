#!/bin/bash

# Python venv
python3 -m venv venv

# React build
cd src/frontend
npm install
npm run build

# Django
cd ..
pip install -r requirements.txt
./venv/bin/python manage.py makemigrations
./venv/bin/python manage.py migrate
./venv/bin/python manage.py collectstatic

# Gunicorn
./venv/bin/gunicorn backend.wsgi