FROM python:3.10-slim-buster

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/code/app/"

COPY ./app /code/app
COPY ./req.txt /code/req.txt

RUN pip install --upgrade pip
RUN pip install -r req.txt

CMD python /code/app/main.py
