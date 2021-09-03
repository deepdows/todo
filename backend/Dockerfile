FROM python:3.9-slim
ADD ./ /app
WORKDIR /app

RUN apt-get update
RUN apt-get install build-essential libpq-dev -y

RUN pip install -r requirements.txt