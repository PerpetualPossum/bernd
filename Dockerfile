FROM python:3.11-buster

RUN pip install poetry==2.1.3

WORKDIR /app

COPY pyproject.toml poetry.lock ./
COPY bernd ./bernd
COPY migrations ./migrations
RUN touch README.md

RUN poetry install

ENTRYPOINT ["poetry", "run", "python", "-m", "bernd.main"]
