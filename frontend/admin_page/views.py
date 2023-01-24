import pandas as pd
from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
import socket
import os
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
import requests
import access

ENVIRONMENT_VARIABLE_PLAYGROUND_PORT = "PLAYGROUND_PORT"
PLAYGROUND_PORT = os.environ.get(ENVIRONMENT_VARIABLE_PLAYGROUND_PORT)

ENVIRONMENT_VARIABLE_PLAYGROUND_HOST = "PLAYGROUND_HOST"
PLAYGROUND_HOST = os.environ.get(ENVIRONMENT_VARIABLE_PLAYGROUND_HOST)

DATABASE_API_POST_FILE_ENDPOINT = "/add_entries/"

@login_required
def adminpage(request: HttpRequest):

    request.session['is_admin'] = False
    is_admin = request.session.get('is_admin') 
    response = render(request, 'admin.html', {"is_admin": is_admin})

    return response

@login_required
def add_entries(request):
    success = 0
    if request.method == 'POST' and 'new_database' in request.FILES:
        files = request.FILES['new_database']
        model = request.POST['model']
        file = files.file
        file_content_binary = file.read()
        file_content_decoded = file_content_binary.decode("utf-8")
        
        data = {'model': model, 'file': file_content_decoded}
        status = access.post_request_to_api(endpoint=DATABASE_API_POST_FILE_ENDPOINT, data=data)
        if status == 200:
            success = 1
        # wrong datatype
        elif status == 415:
            success = 2

    return render(request, 'add_entries.html', {'success': success})



@login_required
def edit_database(request):
    return render(request, 'edit_database.html')

@login_required
def rebuild(request):
    if request.method == 'POST':

        return render(request, 'rebuild.html', {'success': True})
    return render(request, 'rebuild.html', {'success': False})

@login_required
def scraper(request):
    return render(request, 'scraper.html')

@login_required
def playground(request):
    return render(request, 'playground.html', {'playground_host': PLAYGROUND_HOST})