FROM python:3.7-alpine

RUN apk update && apk add libpq
RUN apk add --virtual .build-deps gcc g++ python3-dev musl-dev postgresql-dev

COPY ./requirements.txt /orangered/requirements.txt
WORKDIR /orangered

RUN pip install -r requirements.txt
RUN apk del .build-deps

COPY . /orangered

CMD gunicorn -b 0.0.0.0:5000 app:app
