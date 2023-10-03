FROM python:3.11-alpine
ENV PYTHONUNBUFFERED=1

RUN apk update && apk --no-cache add \
    bash

COPY requirements.txt /app/requirements.txt
COPY utils/extra_requirements.txt /app/utils/extra_requirements.txt

WORKDIR /app
RUN pip install -r requirements.txt

# Install cave_api requirements
COPY ./cave_api/requirements.txt /app/cave_api/requirements.txt
RUN pip install -r cave_api/requirements.txt

COPY docker-entrypoint.sh /usr/local/bin/
ENTRYPOINT ["docker-entrypoint.sh"]
