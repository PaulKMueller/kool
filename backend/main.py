"""This is the backend's main method. It starts the model_api,
the database_api and the playground.
"""

import threading
import os


def run_model_api():
    """Starts the fastapi server for the model_api
    """
    os.system('uvicorn model_api:app --reload --port 8010 --app-dir model_api')


def run_database_api():
    """Starts the fastapi server for the database_api
    """
    os.system('uvicorn database_api:app --reload --port 8020 --host 0.0.0.0 --app-dir database_api')


def run_playground():
    """Starts the streamlit server for the playground
    """
    os.system('streamlit run playground/app.py')


if __name__ == '__main__':
    model_api = threading.Thread(target=run_model_api)
    database_api = threading.Thread(target=run_database_api)
    playground = threading.Thread(target=run_playground)
    model_api.start()
    database_api.start()
    playground.start()
