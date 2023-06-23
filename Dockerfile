FROM python:3.11.3-bullseye
ENV PYTHONUNBUFFERED=1

COPY requirements.txt /app/requirements.txt
COPY utils/extra_requirements.txt /app/utils/extra_requirements.txt
COPY ./cave_api/requirements.txt /app/cave_api/requirements.txt

WORKDIR /app
RUN pip install -r requirements.txt

# Run after pip install to allow caching most of the pip work 
COPY . /app
run pip install -e ./cave_api
