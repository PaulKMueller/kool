FROM python:3.10.8-bullseye

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT python3 run_model_api 0.0.0.0:$FRONTEND_PORT
# ENTRYPOINT ["python", "run_model_api.py"]


