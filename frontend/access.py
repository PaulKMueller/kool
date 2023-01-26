"""Handles requests to backend"""

import os
import requests
from requests import JSONDecodeError

ENVIRONMENT_VARIABLE_DATABASE_API_PORT = "DATABASE_API_PORT"
DATABASE_API_PORT = os.environ.get(ENVIRONMENT_VARIABLE_DATABASE_API_PORT)

MAIN_URL = "http://database_api:" + DATABASE_API_PORT


def get_request_from_api(endpoint):
    """Makes HTTP GET Request to database API

    Args:
        endpoint (str): Endpoint

    Returns:
        json: a JSON Object containing the GET request's answer
    """
    response = requests.get(MAIN_URL + endpoint)
    return response.json()

def post_request_to_api(endpoint, data):
    """Makes HTTP POST Request to database API, mostly used for (re)building data

    Args:
        endpoint (str): Endpoint
        data (json): json data

    Returns:
        int: status code
    """
    
    response = requests.post(MAIN_URL + endpoint, json=data)
    return response.status_code