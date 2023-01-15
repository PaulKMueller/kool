"""Starts the fastapi server for the database_api"""

import threading
import os

ENVIRONMENT_VARIABLE_MODEL_API_PORT = "MODEL_API_PORT"
MODEL_API_PORT = os.environ.get(ENVIRONMENT_VARIABLE_MODEL_API_PORT)

def run_model_api():
    """Starts the fastapi server for the model_api
    """
    os.system('uvicorn model_api:app --reload --port ' + MODEL_API_PORT)


model_api = threading.Thread(target=run_model_api)
model_api.start()

# """ if __name__ == '__main__':
#     database_api = threading.Thread(target=run_database_api)

#     playground = threading.Thread(target=run_playground)

#     database_api.start()
#     playground.start() """
