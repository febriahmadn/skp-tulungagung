FROM python:alpine3.16
COPY . /skpapps
ENV PYTHONUNBUFFERED=1
RUN apk update
RUN apk add postgresql-client
RUN apk add git
RUN pip install --upgrade pip
RUN pip install -r skpapps/requirements/production.txt
WORKDIR /skpapps