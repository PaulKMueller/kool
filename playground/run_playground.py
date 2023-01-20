"""
Starts the streamlit server for the playground
"""

import threading
import os

ENVIRONMENT_VARIABLE_PLAYGROUND_PORT = "PLAYGROUND_PORT"
PLAYGROUND_PORT = os.environ.get(ENVIRONMENT_VARIABLE_PLAYGROUND_PORT)
MAIN_URL = "http://database_api:" + PLAYGROUND_PORT


def run_playground():
    """Starts the streamlit server for the playground
    """
    os.system('streamlit run app.py --server.port ' + PLAYGROUND_PORT)


playground = threading.Thread(target=run_playground)
playground.start()
