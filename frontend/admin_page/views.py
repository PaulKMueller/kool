import pandas as pd
from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
import socket
import os
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
import requests
import json
import access

ENVIRONMENT_VARIABLE_PLAYGROUND_PORT = "PLAYGROUND_PORT"
PLAYGROUND_PORT = os.environ.get(ENVIRONMENT_VARIABLE_PLAYGROUND_PORT)

ENVIRONMENT_VARIABLE_PLAYGROUND_HOST = "PLAYGROUND_HOST"
PLAYGROUND_HOST = os.environ.get(ENVIRONMENT_VARIABLE_PLAYGROUND_HOST)

DATABASE_API_POST_FILE_ENDPOINT = "/add_entries/"
DATABASE_API_REBUILD_ENDPOINT = "/rebuild"
DATABASE_API_ENDPOINT_DATABASE_INFO = "/get_database_info/"
DATABASE_CHANGE_DATABASE_ENDPOINT = "/change_active_database/"

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
def change_database(request):
    success=False
    if request.method == 'POST':
        if 'rebuild' in request.POST:
            model = request.POST['model']
            data = {'model': model}
            status = access.post_request_to_api(endpoint=DATABASE_API_REBUILD_ENDPOINT, data=data)
        
            if status == 200:
                success = True
        elif 'select' in request.POST:
            database = request.POST['database_selector']
            data = {"new_database": database}
            status = access.post_request_to_api(endpoint=DATABASE_CHANGE_DATABASE_ENDPOINT, data=data)

        
    databases = json.loads(access.get_request_from_api(endpoint=DATABASE_API_ENDPOINT_DATABASE_INFO))
    
    return render(request, 'rebuild.html', {'success': success,
                                            'databases': databases})


@login_required
def scraper(request):
    return render(request, 'scraper.html')


@login_required
def playground(request):
    return render(request, 'playground.html', {'playground_host': PLAYGROUND_HOST})
