"""Starts the streamlit server for the playground"""

import threading
import os


def run_playground():
    os.system('streamlit run app.py --server.port 8030')

playground = threading.Thread(target=run_playground)
playground.start() 
