"""Handles requests to backend"""

import requests
import os

ENVIRONMENT_VARIABLE_DATABASE_API_PORT = "DATABASE_API_PORT"
DATABASE_API_PORT = os.environ.get(ENVIRONMENT_VARIABLE_DATABASE_API_PORT)

MAIN_URL = "http://database_api:" + DATABASE_API_PORT


def get_request_from_api(endpoint):
    """Makes HTTP GET Request to database API 

    Args:
        endpoint (str): Endpoint  

    Returns:
        json: a json Object containing the GET Requests answer 
    """
    response = requests.get(MAIN_URL + endpoint)
    return response.json()
