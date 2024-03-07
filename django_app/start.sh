#!/bin/sh
python3 manage.py tailwind start &
python3 manage.py runserver 0.0.0.0:8000