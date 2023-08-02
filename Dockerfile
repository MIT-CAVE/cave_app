FROM python:3.11.3-bullseye
ENV PYTHONUNBUFFERED=1

COPY requirements.txt /app/requirements.txt
COPY utils/extra_requirements.txt /app/utils/extra_requirements.txt

WORKDIR /app
RUN pip install -r requirements.txt

# Install cave_api requirements
COPY ./cave_api/requirements.txt /app/cave_api/requirements.txt
RUN pip install -r cave_api/requirements.txt

# Run after pip install to allow caching most of the pip work 
COPY . /app
RUN pip install -e ./cave_api
