FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update && apt-get install -y --no-install-recommends \
	build-essential \
	python3-dev \
	python3-venv \
	python3-setuptools \
	python3-pip \
	postgresql-client \
	ca-certificates \
    && apt-get -y autoremove && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/*


# Creating a user tu run the process
RUN groupadd -r scrasyncgroup && useradd -r -g scrasyncgroup scrasyncuser
# this line is for alpine
# RUN addgroup -S scrasyncgroup && adduser -S scrasyncuser -G scrasyncgroup

# Copy the current directory contents into the container at /app
COPY djproject /opt/program/djproject
COPY requirements.txt /opt/program
COPY data /opt/program/data

ENV PATH_TO_DATA '/opt/program/data'

RUN chmod +x /opt/program/djproject/run.sh
RUN chmod +x /opt/program/djproject/migrate-and-run.sh

# Install any needed packages specified in requirements.txt
RUN python3 -m pip install --upgrade pip && \
	python3 -m pip install -r /opt/program/requirements.txt

RUN chown -R scrasyncuser:scrasyncgroup /opt/program/djproject

USER scrasyncuser

# Set the working directory to /app
WORKDIR /opt/program/djproject
