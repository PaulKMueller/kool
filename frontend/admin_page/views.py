import json
import os

import pandas as pd
from django.shortcuts import render
from django.http.response import HttpResponse
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.decorators import login_required

import access

ENVIRONMENT_VARIABLE_PLAYGROUND_PORT = "PLAYGROUND_PORT"
PLAYGROUND_PORT = os.environ.get(ENVIRONMENT_VARIABLE_PLAYGROUND_PORT)

ENVIRONMENT_VARIABLE_PLAYGROUND_HOST = "PLAYGROUND_HOST"
PLAYGROUND_HOST = os.environ.get(ENVIRONMENT_VARIABLE_PLAYGROUND_HOST)

ENDPOINT_POST_FILE = "/add_entries/"
ENDPOINT_REBUILD = "/rebuild"
ENDPOINT_DATABASE_INFO = "/get_database_info/"
ENDPOINT_CHANGE_DATABASE = "/change_active_database/"


@login_required
def adminpage(request: HttpRequest) -> HttpResponse:
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
def add_entries(request: HttpRequest) -> HttpResponse:
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
        status = access.post_request_to_api(endpoint=ENDPOINT_POST_FILE,
                                            data=data)
        if status == 200:
            success = 1
        # wrong datatype
        elif status == 415:
            success = 2

    return render(request, 'add_entries.html', {'success': success})


@login_required
def edit_database(request: HttpRequest) -> HttpResponse:
    """
    View for the edit database page on the adminpage.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered admin page.
    """
    return render(request, 'edit_database.html')


@login_required
def get_status_of_db(request: HttpRequest) -> JsonResponse:
    """Gets database info from backend and returns it as JSON

    Args:
        request (HttpRequest): The request object.

    Returns:
        JsonResponse: database info as JSON
    """
    databases = json.loads(access.get_request_from_api(endpoint=ENDPOINT_DATABASE_INFO))
    return JsonResponse(databases)


@login_required
def change_database(request: HttpRequest) -> HttpResponse:
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
        # Select which form was send
        if 'rebuild' in request.POST:
            model = request.POST['model']
            data = {'model': model}
            status = access.post_request_to_api(endpoint=ENDPOINT_REBUILD,
                                                data=data)

            if status == 200:
                success = True
        elif 'select' in request.POST:
            database = request.POST['database_selector']
            data = {"new_database": database}
            status = access.post_request_to_api(endpoint=ENDPOINT_CHANGE_DATABASE,
                                                data=data)

    databases = json.loads(access.get_request_from_api(endpoint=ENDPOINT_DATABASE_INFO))

    return render(request, 'change_database.html', {'success': success,
                                                    'databases': databases})


@login_required
def scraper(request: HttpRequest):
    """
    View for the scraper page on the adminpage.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered admin page.
    """
    return render(request, 'scraper.html')


@login_required
def playground(request: HttpRequest):
    """
    View for the playground on the adminpage.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered admin page.
    """
    return render(request, 'playground.html', {'playground_host': PLAYGROUND_HOST})
