FROM python:3.7-alpine

RUN apk update && apk add libpq

RUN apk add --virtual .build-deps gcc python-dev musl-dev postgresql-dev

ADD requirements.txt /orangered/requirements.txt
RUN pip install -r /orangered/requirements.txt

RUN apk del .build-deps

ADD . /orangered

CMD honcho start -f /orangered/procfile $PROCESSES
