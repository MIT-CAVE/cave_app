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
    bash \
 && addgroup -g 1000 app && adduser -u 1000 -G app -s /bin/sh -D app
ARG SOURCE_DIR
ENV SOURCE_DIR $SOURCE_DIR
ENV PATH $PATH:/usr/local/bin
RUN mkdir -p $SOURCE_DIR
WORKDIR $SOURCE_DIR
ARG PYTHON_VERSION
ENV PYTHON_VERSION $PYTHON_VERSION
COPY --from=builder --chown=app:app /root/.local/ /usr/local/
# USER app
COPY docker-entrypoint.sh /usr/local/bin/
ENTRYPOINT ["docker-entrypoint.sh"]
