import requests

main_url = "http://192.168.143.116:8020"

def get_request_from_api(endpoint):
    response = requests.get(main_url + endpoint)
    return response.json()