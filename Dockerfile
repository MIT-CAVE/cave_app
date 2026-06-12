# syntax = docker/dockerfile:1

# Choose your base image and tag
FROM python:3.13-slim

# Copy the uv and uvx binaries from the official Astral image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set environment variables for optimal Docker caching & execution
ENV UV_LINK_MODE=copy
# Move the virtual environment outside the app directory
# This prevents it from being overwritten by volume mounts (e.g., --volume .:/app)
ENV UV_PROJECT_ENVIRONMENT=/venv
ENV PATH="/venv/bin:$PATH"

# Set python to unbuffered mode
ENV PYTHONUNBUFFERED=1

# Install any additional requirements
# This section can be used to install system dependencies

# Set the working directory to /app
WORKDIR /app/

# Install Core Cave App Python Requirements
# Copying uv.lock ensures deterministic builds
COPY pyproject.toml uv.lock ./

# Sync dependencies without installing the project itself
# This maximizes layer caching when source code changes
RUN uv sync --no-install-project --extra api
