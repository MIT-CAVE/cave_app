# syntax = docker/dockerfile:1

################ Settings ################
# Choose your base image and tag
FROM python:3.13-slim
################ Settings ################

# Set python to unbuffered mode
ENV PYTHONUNBUFFERED=1

# Install any additional requirements
# This section can be used to install system dependencies

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
