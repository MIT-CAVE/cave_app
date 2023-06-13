FROM python:3.11.3-bullseye

COPY requirements.txt /app/requirements.txt
COPY utils/extra_requirements.txt /app/utils/extra_requirements.txt
COPY cave_api /app/cave_api
WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app
