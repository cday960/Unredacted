# Docker setup
Instead of having to setup each component individually, the docker-compose command from root in the project directory will start both the website and api for you.
```bash
docker-compose up --build
```


# Django Webapp

## Virtualenv setup 
Create the python virtual env and install packages
```bash
cd django_app
virtualenv --clear .venv
source .venv/bin/activate 
pip install -r requirements.txt
```

## Installing Tailwind
```bash
python3 manage.py tailwind install
```

## Start server
```bash
sh start.sh
```

# Flask API

## Virtualenv setup 
Create the python virtual env and install packages
```bash
cd django_app
virtualenv --clear .venv
source .venv/bin/activate 
pip install -r requirements.txt
```

## Start server
```bash
python3 src/flask_api/app.py
```