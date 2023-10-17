# syntax = docker/dockerfile:1

################ Settings ################
# Choose your base image and tag
# Alpine Based Python Image
ARG ROOT_CONTAINER=python:3.12-alpine
# Debian Based Python Image
# ARG ROOT_CONTAINER=python:3.12-bullseye
################ Settings ################


# Create a builder image to install any requirements
FROM ${ROOT_CONTAINER}

# Set python to unbuffered mode
ENV PYTHONUNBUFFERED=1

# Install any additional requirements
# EG: Use bash for alpine images / install some build tools and cryptography dependencies
RUN apk update && apk --no-cache add bash build-base libffi-dev

# Set the working directory to /app
WORKDIR /app/

# Install Core Cave App Python Requirements
COPY ./requirements.txt /app/requirements.txt
COPY ./utils/extra_requirements.txt /app/utils/extra_requirements.txt
RUN pip install -r /app/requirements.txt

# Install Cave API Python Requirements
COPY ./cave_api/requirements.txt /app/cave_api/requirements.txt
RUN pip install -r /app/cave_api/requirements.txt

# Copy the current directory contents into the container at /app
COPY cave_api/pyproject.toml /app/cave_api/pyproject.toml
COPY cave_api/cave_api/__init__.py /app/cave_api/cave_api/__init__.py
RUN pip install -e /app/cave_api
