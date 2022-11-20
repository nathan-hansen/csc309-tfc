#!/usr/bin/bash

python3.10 -m venv env
source env/bin/activate
python3 -m pip install -r requirements.txt --force-reinstall
python3 manage.py makemigrations
python3 manage.py migrate

