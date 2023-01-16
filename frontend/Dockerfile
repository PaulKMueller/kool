FROM python:3.10.8-bullseye

ARG FRONTEND_PORT

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# Starts the Frontend on Port
# TODO Make this beautiful
ENTRYPOINT ["python3", "manage.py", "runserver", "0.0.0.0:8000"]


