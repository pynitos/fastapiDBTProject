FROM python:3.13-slim as base_image

ENV PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_VERSION=1.8

# Install system dependencies
RUN apt-get update && \
    apt-get install -y libpq-dev gcc && \
    pip install "poetry==$POETRY_VERSION"

# Copy project files
WORKDIR /code
COPY poetry.lock .
COPY pyproject.toml .
COPY ./docker/user-ms.sh .
COPY user_ms.env .
COPY ./src/user_ms/ ./src/user_ms/

# Expose port 8000
EXPOSE 8000

# Entrypoint script for migrations import
ENTRYPOINT ["bash", "./user-ms.sh"]


FROM base_image as prod_image

# Install project's dependencies
RUN poetry config virtualenvs.create false && poetry install --without dev diary-ms --no-interaction --no-root

# Run server
WORKDIR /code/todolist
CMD ["gunicorn", "src.user_ms.wsgi", "-w", "2", "-b", "0.0.0.0:8000"]

FROM base_image as dev_image

# Install project's dependencies
RUN poetry config virtualenvs.create false && poetry install --without diary-ms --no-interaction --no-root

# Run server

CMD ["python", "src/user_ms/manage.py", "runserver", "0.0.0.0:8000"]