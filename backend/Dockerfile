FROM python:3.6-alpine

WORKDIR ./app

COPY ./config ./config
COPY ./src ./src
COPY ./wsgi.py .
COPY ./Makefile .
COPY ./requirements.txt .
COPY ./LICENSE .

RUN apk update && \
    apk add make

RUN make build
CMD ["make", "run"]

HEALTHCHECK CMD curl --fail http://localhost:5000/api/healthcheck || exit 1
