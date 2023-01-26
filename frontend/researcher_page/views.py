"""This module contains the views for the result_page app.
"""

import json
from typing import Optional
from django.shortcuts import render, redirect
from result_page.models import Author
import access
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.contrib.auth.decorators import login_required

def researcher(request: HttpRequest, id: Optional[int] = None) -> HttpResponse:
    """Renders the researcher page.
    If ?q=... exists its preferred, else id is used. When no authors are
    found, the user is informed in frontend.

    Args:
        request (HttpRequest): The request object.
        int: ID of the competency. Defaults to None.

    Returns:
        HttpResponse: The rendered researcher page.
    """
    all_competencies = access.get_request_from_api("/all_competencies/")

    return render(request, 'researcher_page.html', {'all_competencies': json.dumps(all_competencies)})
