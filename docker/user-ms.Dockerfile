FROM python:3.13-slim AS base_image

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


FROM base_image as dev_image
RUN poetry config virtualenvs.create false && poetry install --without dev --without diary-ms --no-interaction --no-root

COPY user_ms.env .
COPY ./src/user_ms/ ./src/user_ms/

WORKDIR /code/src/user_ms/
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


FROM base_image as prod_image
RUN poetry config virtualenvs.create false && poetry install --without dev --without diary-ms --no-interaction --no-root

COPY user_ms.env .
COPY ./src/user_ms/ ./src/user_ms/
EXPOSE 8000

CMD ["gunicorn", "src.user_ms.wsgi", "-w", "2", "-b", "0.0.0.0:8000"]
