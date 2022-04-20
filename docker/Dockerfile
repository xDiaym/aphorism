FROM python:3.10 as development_build

ARG FLASK_ENV

ENV FLASK_ENV=${FLASK_ENV} \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    PATH="$PATH:/root/.poetry/bin"

# Install system dependencies
RUN apt update && apt upgrade -y \
    # Install dependencies  \
    && apt install libpq-dev \
    # Install poetry package manager
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - \
    && poetry --version \
    # Clean build cache
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY ./docker/entrypoint.sh /entrypoint.sh

# Setting up proper permissions:
RUN chmod +x '/entrypoint.sh' \
      && groupadd -r web && useradd -d /code -r -g web web \
      && chown web:web -R /code/ \
      && mkdir -p /var/www/media/audio \
      && chown web:web /var/www/media/audio

# Copy only requirements, to cache them in docker layer
COPY --chown=web:web ./poetry.lock ./pyproject.toml /code/

# Install app dependencies
RUN echo "Use $FLASK_ENV" \
    && poetry install $(if [ $FLASK_ENV = "production" ]; then echo '--no-dev'; fi) --no-interaction \
    && if [ $FLASK_ENV = "production" ]; then rm -rf $POETRY_CACHE_DIR; fi

RUN chown web:web /usr/local/bin/flask


USER web

ENTRYPOINT ["/entrypoint.sh"]


# Production only build
FROM development_build AS production_build
COPY --chown=web:web . /code

