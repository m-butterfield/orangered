FROM python:3.7-alpine

COPY . /orangered
WORKDIR /orangered

RUN apk update && apk add libpq
RUN apk add --virtual .build-deps gcc python-dev musl-dev postgresql-dev
RUN pip install -r requirements.txt
RUN apk del .build-deps

CMD honcho start -f /orangered/procfile $PROCESSES
