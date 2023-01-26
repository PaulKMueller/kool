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
    When no authors are found, the user is informed in frontend.

    Args:
        request (HttpRequest): The request object.
        int: ID of the competency. Defaults to None.

    Returns:
        HttpResponse: The rendered researcher page.
    """



    found_id = False
    author_first_name = None
    author_last_name = None
    competencies = None

    if id:
        author = access.get_request_from_api("/author_by_id/" + str(id))
        author_first_name = author[0]
        author_last_name = author[1]
        competencies = access.get_request_from_api("/competencies_by_author_id/{author_id}")
    
    if author_first_name and author_last_name:
        found_id = True

    all_competencies = access.get_request_from_api("/all_competencies/")

    return render(request, 'researcher_page.html', {'has_found': found_id,
                                                    'id': id,
                                                    'competencies': competencies,
                                                    'author_first_name': author_first_name,
                                                    'author_last_name': author_last_name,
                                                    'all_competencies': json.dumps(all_competencies)})
