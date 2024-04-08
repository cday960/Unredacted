FROM python:3.9.19-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

ADD . /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# Command to run the Flask application
CMD ["flask", "run", "--host=127.0.0.1", "--port=5000", "--debug"]