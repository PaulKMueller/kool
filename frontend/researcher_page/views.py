"""This module contains the views for the result_page app.
"""

import json
from typing import Optional
from django.shortcuts import render, redirect
from researcher_page.models import Author, Abstract, Competency
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
    author = None
    competencies = []
    author_first_name = None
    author_last_name = None
    author_abstracts = []

    if id:
        author_response = access.get_request_from_api("/author_by_id/" + str(id))
        author_first_name = author_response[0]
        author_last_name = author_response[1]

        if author_first_name and author_last_name:
            found_id = True
            author_id = id

            author_competencies = access.get_request_from_api("/competencies_by_author_id/" + str(author_id))
            for competency in author_competencies:
                competency_id = competency[0]
                ranking = access.get_request_from_api("/ranking_score/" + str(author_id) + "/" + str(competency_id))

                relevant_abstract_ids = access.get_request_from_api("/abstracts_with_competency_by_author/" + str(competency_id) + "/" + str(author_id))
                relevant_abstracts = []
                for abstract_id in relevant_abstract_ids:
                    abstract = access.get_request_from_api("/abstract_by_id/" + str(abstract_id[0]))
                    relevant_abstracts.append(Abstract(abstract[0], abstract[1], abstract[2], abstract[3], abstract[4], abstract[5]))

                competencies.append(Competency(competency_id, competency[1], competency[2], ranking, relevant_abstracts))
                
            author = Author(id=author_id, first_name=author_first_name, last_name=author_last_name, competencies=competencies)
    
    
    


    return render(request, 'researcher_page.html', {'has_found': found_id,
                                                    'id': id,
                                                    'competencies': competencies,
                                                    'author': author
                                                    })



