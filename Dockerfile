# this should be ran using python:3.6
FROM python:3.6

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# the redis host
ENV REDIS_HOST_NAME 'redis'

RUN chmod +x /app/celery.sh

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt


