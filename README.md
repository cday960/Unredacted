# Unredacted

## Install
Create the python virtual env and install packages
```python
python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```

## Start server
Go into the site folder, run these 2 commands in different terminal instances
```python
python manage.py runserver <port>
```
```python
python manage.py tailwind start
```

Both should be running on the same port, can also omit the port for the default 8000.
