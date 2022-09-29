FROM docker.io/python:3.10-buster
WORKDIR /app

RUN apt update && \
  curl -sSL https://install.python-poetry.org | python3 -

ENV POETRY_VERSION=1.2.1

RUN pip install "poetry==$POETRY_VERSION"


COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

RUN poetry config virtualenvs.create false --local
RUN poetry install --no-root

COPY . /app

CMD ["python", "/app/main.py"]
