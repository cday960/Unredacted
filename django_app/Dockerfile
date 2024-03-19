# Use an official Python runtime as a parent image
FROM python:3.9

LABEL image.authors = "Luke Schaefer sluke817@gmail.com"

RUN apt-get update
RUN apt-get -y upgrade

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the application code into the container
ADD . /app/

# Install Node.js
RUN apt-get install -y nodejs npm

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 to allow communication to/from server
EXPOSE 8000

RUN python manage.py tailwind install

# Command to run the Django development server
CMD ["sh", "start.sh"]