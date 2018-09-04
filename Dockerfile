FROM python:2
ENV PYTHONUNBUFFERED 1
RUN mkdir /matcher

WORKDIR /matcher
ADD requirements.txt /matcher/
RUN pip install -r requirements.txt
ADD . /matcher/
