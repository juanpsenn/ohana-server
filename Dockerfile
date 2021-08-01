FROM python:3.9.6-alpine
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt /app/

RUN apk add python3-dev build-base
RUN pip install -r ./requirements.txt

COPY . /app/

CMD python3 manage.py runserver 0.0.0.0:8000
