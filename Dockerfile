# syntax=docker/dockerfile:1

# Start your image with a node base image
FROM ubuntu:22.04

# Update Packages And Install Common Software Properties
RUN apt-get update && apt-get upgrade -y && apt-get install -y software-properties-common
# Add the deadsnakes python PPA
RUN add-apt-repository ppa:deadsnakes/ppa

# Install TZData
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get install tzdata -y
# Install new packages
RUN apt-get install postgresql postgresql-contrib python3.11 curl -y
# Install pip
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11
# Install virtualenv
RUN python3.11 -m pip install virtualenv
# Start up postgres
RUN service postgresql start

# Create an application directory and setup the app
RUN mkdir -p /app
WORKDIR /app
RUN python3.11 -m virtualenv venv && source venv/bin/activate && pip install -r requirements.txt --require-virtualenv

# TODO - Figure out the database setup process

# TODO - Collect static files

# TODO - Start the server

# Specify that the application in the container listens on port 8000
EXPOSE 8000

# Start the app using serve command
# CMD [ "python3.11", "manage.py", "runserver" ]