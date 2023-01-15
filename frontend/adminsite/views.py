import pandas as pd
from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
import socket
import os

ENVIRONMENT_VARIABLE_PLAYGROUND_PORT = "PLAYGROUND_PORT"
PLAYGROUND_PORT = os.environ.get(ENVIRONMENT_VARIABLE_PLAYGROUND_PORT)


def adminpage(request):
    return render(request, 'admin.html')

def add_entries(request):
    if request.method == 'POST' and 'new_database' in request.FILES:
        myfile = request.FILES['new_database']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'admin.html')
    return render(request, 'add_entries.html')


def edit_database(request):
    return render(request, 'edit_database.html')


def rebuild(request):
    return render(request, 'rebuild.html')


def scraper(request):
    return render(request, 'scraper.html')


def playground(request):
    url = "http://" + str(socket.gethostbyname("playground")) + ":" + str(PLAYGROUND_PORT)
    print(url)
    return render(request, 'playground.html', {"url": url})