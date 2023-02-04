"""
Starts the fastapi server for the database_api
"""

import threading
import os
from db_creation import database_from_csv

ENVIRONMENT_VARIABLE_DATABASE_API_PORT = "DATABASE_API_PORT"
DATABASE_API_PORT = os.environ.get(ENVIRONMENT_VARIABLE_DATABASE_API_PORT)


def run_database_api():
    """Starts the fastapi server for the database_api
    """
    # change to production server when deploying 
    os.system('uvicorn database_api:app --reload --port ' + DATABASE_API_PORT
              + ' --host 0.0.0.0')


database_api = threading.Thread(target=run_database_api)
database_api.start()
