# syntax = docker/dockerfile:1

# Choose your base image and tag
FROM python:3.13-slim

# Copy the uv and uvx binaries from the official Astral image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set environment variables for optimal Docker caching & execution
ENV UV_LINK_MODE=copy

# Set python to unbuffered mode
ENV PYTHONUNBUFFERED=1

# Install any additional requirements
# This section can be used to install system dependencies

# Set the working directory to /app
WORKDIR /app/
COPY ./cave_api/__init__.py /app/cave_api/__init__.py

# Install Core Cave App Python Requirements
COPY ./pyproject.toml /app/pyproject.toml
RUN uv sync --extra cave_api
