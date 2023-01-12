FROM python:3.10.8-bullseye
RUN echo "Test"
WORKDIR /usr/src/app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python", "run_playground.py"]


