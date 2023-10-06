
FROM python:3.10-slim


WORKDIR /tgtranslatebot

COPY ./ /tgtranslatebot/
COPY pyproject.toml /tgtranslatebot/

ENV PYTHONPATH=${PYTHONPATH}:${PWD}
RUN apt-get update \
    && apt-get -y install libpq-dev python-dev-is-python3 gcc


RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
CMD python -m app.main
