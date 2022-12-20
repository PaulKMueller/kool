from django.shortcuts import render
import requests
import json

main_url = "http://192.168.123.116:8020"

def get_request_from_api(url):
    for i in range(5):
        try:
            response = requests.get(url)
            return response.json()
        except:
            time.sleep(2)
            continue
    return "connection failed"


def home(request):
    req_all_comp = main_url + "/all_competencies/"
    competencies = get_request_from_api(req_all_comp)
    print(json.dumps(competencies))
    return render(request, 'home.html', {'competencies': json.dumps(competencies)})

def aboutkoolpage(request):
    return render(request, 'aboutkool.html')


