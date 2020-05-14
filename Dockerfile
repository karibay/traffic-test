FROM python:3.8.1
ENV PYTHONBUFFERED 1

RUN mkdir /credits
WORKDIR /credits
COPY requirements.txt /credits/

RUN pip install -r requirements.txt

COPY . /credits/ 

