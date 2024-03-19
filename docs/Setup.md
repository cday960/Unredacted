# Docker setup
Make sure to load a .env file with the appropriate API keys
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
cd atlas
virtualenv --clear .venv
source .venv/bin/activate 
pip install -r requirements.txt
```

## Start server
```bash
flask app run
```