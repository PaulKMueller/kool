import pandas as pd
from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
import socket
import os
from django.http import HttpRequest, JsonResponse
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
    """
    View for the adminpage.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered admin page.
    """
    response = render(request, 'admin.html')

    return response


@login_required
def add_entries(request: HttpRequest):
    """View for the add entries page on the adminpage. Note that there is a
    submit button which uploads a new csv with new entries and the model with
    which the entries should be computated. This is handled in the backend and
    returns if the action was successful.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered add entries page.
    """
    success = 0
    if request.method == 'POST' and 'new_database' in request.FILES:
        files = request.FILES['new_database']
        model = request.POST['model']
        file = files.file
        file_content_binary = file.read()
        file_content_decoded = file_content_binary.decode("utf-8")

        data = {'model': model, 'file': file_content_decoded}
        status = access.post_request_to_api(endpoint=DATABASE_API_POST_FILE_ENDPOINT,
                                            data=data)
        if status == 200:
            success = 1
        # wrong datatype
        elif status == 415:
            success = 2

    return render(request, 'add_entries.html', {'success': success})


@login_required
def edit_database(request):
    """
    View for the edit database page on the adminpage.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered admin page.
    """
    return render(request, 'edit_database.html')


@login_required
def get_status_of_db(request):
    databases = json.loads(access.get_request_from_api(endpoint=DATABASE_API_ENDPOINT_DATABASE_INFO))
    return JsonResponse(databases)


@login_required
def change_database(request):
    """View the change database page on the adminpage. Note that there
    are two buttons. One is for rebuilding the database with chosen model.
    The other one is for selecting the displayed database.
    Returns if action was successful and the active database.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered admin page.
    """

    success = False
    if request.method == 'POST':
        if 'rebuild' in request.POST:
            model = request.POST['model']
            data = {'model': model}
            status = access.post_request_to_api(endpoint = DATABASE_API_REBUILD_ENDPOINT, data=data)

            if status == 200:
                success = True
        elif 'select' in request.POST:
            database = request.POST['database_selector']
            data = {"new_database": database}
            status = access.post_request_to_api(endpoint = DATABASE_CHANGE_DATABASE_ENDPOINT, data=data)

    databases = json.loads(access.get_request_from_api(endpoint = DATABASE_API_ENDPOINT_DATABASE_INFO))

    return render(request, 'change_database.html', {'success': success,
                                            'databases': databases})


@login_required
def scraper(request):
    """
    View for the scraper page on the adminpage.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered admin page.
    """
    return render(request, 'scraper.html')


@login_required
def playground(request):
    """
    View for the playground on the adminpage.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered admin page.
    """
    return render(request, 'playground.html', {'playground_host': PLAYGROUND_HOST})
