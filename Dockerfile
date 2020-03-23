FROM python:3
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app
RUN apt-get update && apt-get install postgresql-11 gcc python3-dev musl-dev -y
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /usr/src/app/