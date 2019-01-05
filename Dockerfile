FROM python:2.7
MAINTAINER Yuzongkun<beaock@gmail.com>

WORKDIR /app

RUN pip install -v pip-tools==1.9.0

ADD ./docker/start-server.sh /app/docker/start-server.sh
ADD ./requirements.txt requirements.txt
RUN pip install -r /app/requirements.txt