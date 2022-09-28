FROM docker.io/python:3.10
WORKDIR /app

RUN apt update && \
  apt install curl -y && \
  curl -sSL https://install.python-poetry.org | python3 -

ONBUILD COPY pyproject.toml pyproject.toml
ONBUILD COPY poetry.lock poetry.lock
ONBUILD RUN poetry install

COPY . /app

CMD ["uvicorn", "main:app"]
