"""Starts the fastapi server for the database_api"""

import threading
import os

ENVIRONMENT_VARIABLE_MODEL_API_PORT = "MODEL_API_PORT"
MODEL_API_PORT = os.environ.get(ENVIRONMENT_VARIABLE_MODEL_API_PORT)


def run_model_api():
    """Starts the fastapi server for the model_api
    """
    os.system('uvicorn model_api:app --reload --port ' + MODEL_API_PORT  + ' --host 0.0.0.0')


model_api = threading.Thread(target=run_model_api)
model_api.start()
