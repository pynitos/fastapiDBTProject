FROM python:3.13-slim AS base_image

ENV PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_VERSION=1.8.4

# Install system dependencies
RUN apt-get update && \
    apt-get install -y libpq-dev gcc && \
    pip install "poetry==$POETRY_VERSION"

WORKDIR /code/
# Install project's dependencies
COPY pyproject.toml .
RUN poetry config virtualenvs.create false && \
poetry install --without dev --without user-ms --without diary-bot --no-interaction --no-root 

COPY alembic.ini .
COPY pre_start.py .
COPY prestart.sh .
COPY .env .
COPY ./src/__init__.py ./src/__init__.py
COPY ./src/diary_ms/ ./src/diary_ms/

EXPOSE 8000

ENTRYPOINT [ "bash", "prestart.sh"]

FROM base_image AS prod_image

CMD ["fastapi", "run", "--workers", "4", "./src/diary_ms/main/web.py"]  

FROM base_image AS dev_image

CMD ["fastapi", "run", "--reload", "./src/diary_ms/main/web.py"]
