FROM python:3.9.19-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

ADD . /app/

RUN apt-get clean
RUN apt-get update
# RUN apt-get -y upgrade
RUN apt-get install -y nodejs npm --fix-missing
RUN pip3 install --no-cache-dir -r requirements.txt
RUN python3 manage.py tailwind install

EXPOSE 8000

CMD ["sh", "start.sh"]