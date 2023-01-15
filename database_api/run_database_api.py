"""Starts the fastapi server for the database_api"""

import threading
import os


def run_database_api():
    os.system('uvicorn database_api:app --reload --port 8020 --host 0.0.0.0')


database_api = threading.Thread(target=run_database_api)
database_api.start()
