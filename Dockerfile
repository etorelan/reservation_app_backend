# Use an official Python runtime as a parent image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y redis-server

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . /app/

# Start Celery worker and Celery beat
CMD python -m celery -A netflix_clone_backend worker & sleep 20 & python -m celery -A netflix_clone_backend beat & python manage.py runserver 0.0.0.0:8000