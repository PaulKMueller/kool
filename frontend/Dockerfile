FROM python:3.10.8-bullseye

ARG FRONTEND_PORT

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# Starts the Frontend on Port FRONTEND_PORT
# shell form so passing of ENV works
ENTRYPOINT python3 manage.py runserver 0.0.0.0:$FRONTEND_PORT


