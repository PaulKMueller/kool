from django.shortcuts import render
import requests
import json
import time
import access

def home(request):
    competencies = access.get_request_from_api("/all_competencies/")
    return render(request, 'home.html', {'all_competencies': json.dumps(competencies)})

def aboutkoolpage(request):
    return render(request, 'aboutkool.html')


