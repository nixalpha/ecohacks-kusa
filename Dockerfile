FROM python:3.9-slim-bullseye

WORKDIR /app
COPY ./ .

RUN pip install -r requirements.txt

CMD exec gunicorn --bind :$PORT --workers 1 --threads 4 --timeout 0 routes:app
