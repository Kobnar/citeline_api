FROM ubuntu
MAINTAINER Konrad R.K. Ludwig <konrad.rk.ludwig@gmail.com>

# Update package index and install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    git \
    python3 \
    python3-dev \
    python3-setuptools

# Clone and install Stackcite Database Schema
RUN git clone -b dev https://github.com/Kobnar/stackcite_db.git /stackcite_db
RUN cd /stackcite_db && python3 setup.py develop

# Copy and install Stackcite API
COPY . /stackcite_api
RUN cd /stackcite_api && python3 setup.py develop

# Serve Stackcite API
WORKDIR /stackcite_api
CMD pserve development.ini