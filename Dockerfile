# syntax = docker/dockerfile:1
ARG PYTHON_VERSION=3.11
ARG SOURCE_DIR=/app/

# builder image
FROM python:${PYTHON_VERSION}-alpine as builder
COPY ./requirements.txt /app/requirements.txt
COPY ./utils/extra_requirements.txt /app/utils/extra_requirements.txt
RUN pip install --user --requirement /app/requirements.txt
# Install cave_api requirements
COPY ./cave_api/requirements.txt /app/cave_api/requirements.txt
RUN pip install --user --requirement /app/cave_api/requirements.txt


FROM python:${PYTHON_VERSION}-alpine
RUN apk update && apk --no-cache add \
    bash
ARG SOURCE_DIR
ENV SOURCE_DIR $SOURCE_DIR
ENV PATH $PATH:/usr/local/bin
RUN mkdir -p $SOURCE_DIR
WORKDIR $SOURCE_DIR
COPY --from=builder /root/.local/ /usr/local/
COPY docker-entrypoint.sh /usr/local/bin/
ENTRYPOINT ["docker-entrypoint.sh"]
