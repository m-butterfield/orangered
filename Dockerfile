FROM python:3.10-slim as python
ENV PYTHONUNBUFFERED=true
WORKDIR /orangered

FROM python as poetry
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN apt-get update \
    && apt-get -y install libpq-dev gcc
RUN python -c 'from urllib.request import urlopen; print(urlopen("https://install.python-poetry.org").read().decode())' | python -
COPY ./pyproject.toml /orangered/pyproject.toml
RUN poetry install --no-interaction --no-ansi -vvv

FROM python as server
ENV PATH="/orangered/.venv/bin:$PATH"
COPY --from=poetry /orangered /orangered
COPY . /orangered
CMD gunicorn -w 4 -b :8000 app:app
