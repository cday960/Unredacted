# Note about MongoDB
For the application to work properly you need your IP address added to MongoDB site. It will not run at all without this connection.
If you have questions about how to do that ask Luke or Landon


# Django Webapp

## Virtualenv setup 
Create the python virtual env and install packages
```bash
virtualenv --clear .venv
source .venv/bin/activate 
pip install -r requirements.txt
```

## Export the ATLAS_URL environment variable
```bash
    export ATLAS_URL=http://127.0.0.1:5000/atlas
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
## Export the all environment variables. Check discord for these variables
```bash
export NA_API_KEY=<KEY>
export NLP_API_KEY=<KEY>
export MONGO_URI=<URI>
```

## Start server
```bash
flask app run
```