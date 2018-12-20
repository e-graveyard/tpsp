FROM python:3.6-alpine
MAINTAINER Caian R. Ertl <caianrais@pm.me>

RUN apk add --update build-base libxml2-dev libxslt-dev
RUN rm -rf /var/cache/apk/*

RUN pip3 install tpsp

ENTRYPOINT ["tps"]
