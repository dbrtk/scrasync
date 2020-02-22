FROM python:3.8

# Creating a user tu run the process
RUN groupadd -r scrasyncuser && useradd -r -g scrasyncuser scrasyncuser

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# rabbitmq and redis hosts
ENV BROKER_HOST_NAME 'rabbitmq'
ENV REDIS_HOST_NAME 'redis'

RUN chmod +x /app/celery.sh

# Install any needed packages specified in requirements.txt
RUN pip install -U pip && pip install .

RUN chown -R scrasyncuser:scrasyncuser /app

USER scrasyncuser
