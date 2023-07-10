FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_HOME="/opt/poetry"

WORKDIR /app

RUN curl -sSL https://install.python-poetry.org | python3 - \
    && cd /usr/local/bin \
    &&  ln -s /opt/poetry/bin/poetry \
    && poetry config virtualenvs.create false \
    && poetry config virtualenvs.in-project false

COPY ./pyproject.toml ./poetry.lock* /app/
RUN poetry install

COPY . /app

COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app:$PYTHONPATH

CMD ["/docker-entrypoint.sh"]
