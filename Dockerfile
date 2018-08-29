FROM python:2
ENV PYTHONUNBUFFERED 1
RUN mkdir /matcher
RUN apt-get update \
  && apt-get install -y postgresql postgresql-contrib libpq-dev postgresql-client postgresql-client-common \
  && apt-get install sudo \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
WORKDIR /matcher
ADD requirements.txt /matcher/
RUN pip install -r requirements.txt
ADD . /matcher/
