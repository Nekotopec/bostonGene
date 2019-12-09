FROM python:3.7.5-alpine

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY ./bostonGene /code/bostonGene
COPY ./md5_sum /code/md5_sum
COPY manage.py /code
COPY pytest.ini /code
RUN pytest -x -v

