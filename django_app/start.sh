#!/bin/bash
# virtualenv --clear .venv
# source .venv/bin/activate 
# pip install -r requirements.txt
python3 manage.py tailwind start &
python3 manage.py runserver 0.0.0.0:8000