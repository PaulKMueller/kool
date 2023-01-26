import pandas as pd
from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
import socket
import os
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required

ENVIRONMENT_VARIABLE_PLAYGROUND_PORT = "PLAYGROUND_PORT"
PLAYGROUND_PORT = os.environ.get(ENVIRONMENT_VARIABLE_PLAYGROUND_PORT)


ENVIRONMENT_VARIABLE_PLAYGROUND_HOST = "PLAYGROUND_HOST"
PLAYGROUND_HOST = os.environ.get(ENVIRONMENT_VARIABLE_PLAYGROUND_HOST)


@login_required
def adminpage(request: HttpRequest):

    request.session['is_admin'] = False
    is_admin = request.session.get('is_admin') 
    response = render(request, 'admin.html', {"is_admin": is_admin})

    return response


@login_required
def add_entries(request):
    if request.method == 'POST' and 'new_database' in request.FILES:
        myfile = request.FILES['new_database']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'admin.html')
    return render(request, 'add_entries.html')


@login_required
def edit_database(request):
    return render(request, 'edit_database.html')


@login_required
def rebuild(request):
    return render(request, 'rebuild.html')


@login_required
def scraper(request):
    return render(request, 'scraper.html')


@login_required
def playground(request):
    return render(request, 'playground.html', {'playground_host': PLAYGROUND_HOST})
