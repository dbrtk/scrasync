FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update && apt-get install -y --no-install-recommends \
	build-essential \
	python3-dev \
	python3-venv \
	python3-setuptools \
	python3-pip \
	ca-certificates \
    && apt-get -y autoremove && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/*


# Creating a user tu run the process
RUN groupadd -r scrasyncgroup && useradd -r -g scrasyncgroup scrasyncuser
# this line is for alpine
# RUN addgroup -S scrasyncgroup && adduser -S scrasyncuser -G scrasyncgroup

# Copy the current directory contents into the container at /app
COPY . /app

RUN chmod +x /app/celery.sh

# Install any needed packages specified in requirements.txt
RUN pip install -U pip && pip install /app

RUN chown -R scrasyncuser:scrasyncgroup /app

USER scrasyncuser

# Set the working directory to /app
WORKDIR /app/djproject
