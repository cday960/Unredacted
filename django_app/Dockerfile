FROM python:3.9.19-slim

# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

RUN apt-get clean
RUN apt-get update
# RUN apt-get -y upgrade
RUN apt-get install -y npm

WORKDIR /app

ADD . /app/

RUN apt-get install -y npm
RUN pip3 install -r requirements.txt
RUN python3 manage.py tailwind install

EXPOSE 8000

CMD ["sh", "start.sh"]