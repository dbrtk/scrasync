FROM python:latest

# Creating a user tu run the process
RUN groupadd -r scrasyncgroup && useradd -r -g scrasyncgroup scrasyncuser
# this line is for alpine
# RUN addgroup -S scrasyncgroup && adduser -S scrasyncuser -G scrasyncgroup

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN chmod +x /app/celery.sh

# Install any needed packages specified in requirements.txt
RUN python -m pip install -U pip && python -m pip install /app

RUN chown -R scrasyncuser:scrasyncgroup /app

USER scrasyncuser
