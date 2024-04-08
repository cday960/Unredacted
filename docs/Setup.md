# Note about MongoDB
For the application to work properly you need your IP address added to MongoDB site. It will not run at all without this connection.
If you have questions about how to do that ask Luke or Landon


# Docker setup
Make sure to load atlas .env file with the appropriate API keys
```bash
docker-compose up --build
```


# Django Webapp

## Virtualenv setup 
Create the python virtual env and install packages
```bash
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
Then export the API keys and mongo URI. Check discord for those values

## Start server
```bash
flask app run
```