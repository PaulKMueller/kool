"""Defines the views used in the landing page.
"""

import django.http
import django.http.response
import json
from django.shortcuts import render
import access
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse


def home(request: HttpRequest) -> HttpResponse:
    """Renders the home page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered home page.
    """
    competencies = access.get_request_from_api("/all_competencies/")
    return render(request, 'home.html',
                  {'all_competencies': json.dumps(competencies)})


def aboutkoolpage(request: HttpRequest) -> HttpResponse:
    """Renders the about kool page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The rendered about kool page.
    """
    return render(request, 'about_kool.html')
