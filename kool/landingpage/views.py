import json
from django.shortcuts import render
import access


def home(request):
    '''Renders homepage'''
    competencies = access.get_request_from_api("/all_competencies/")
    return render(request, 'home.html',
                  {'all_competencies': json.dumps(competencies)})


def aboutkoolpage(request):
    '''Renders About Kool Page'''
    return render(request, 'aboutkool.html')
