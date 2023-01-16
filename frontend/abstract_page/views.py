from django.shortcuts import render
import requests
from abstract_page.models import Abstract, Author, Competency
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
import json
# Create your views here.
import access
from typing import Optional


def abstract_page(request: HttpRequest, id: int, auth_id: Optional[int] = None) -> HttpResponse:
    """Retrieves Abstract and corresponding competencies and authors of the
    abstract. Searches for detailed author. Passes this info to template.

    Args:
        request (HttpRequest): HTTP Request 
        id (int): id of the abstract which will be shown on the page
        auth_id (int, optional): _description_. Defaults to None.

    Returns:
        HttpResponse: The rendered results page.
    """

    ABSTRACT_BY_ID_ENDPOINT = "/abstract_by_id/"
    AUTHOR_BY_ABSTRACT_ID_ENDPOINT = "/author_by_abstract_id/"
    COMPETENCIES_BY_ABSTRACT_ID_ENDPOINT = "/competencies_by_abstract_id/"
    COMPETENCIES_BY_AUTHOR_ID_ENDPOINT = "/competencies_by_author_id/"

    abstract_db_entry = access.get_request_from_api(ABSTRACT_BY_ID_ENDPOINT
                                                    + str(id))
    # Depends on order of results in Database API
    abstract = Abstract(id=abstract_db_entry[0],
                        year=abstract_db_entry[1],
                        title=abstract_db_entry[2],
                        content=abstract_db_entry[3],
                        doctype=abstract_db_entry[4],
                        institution=abstract_db_entry[5])
    authors_db_entry = access.get_request_from_api(
        AUTHOR_BY_ABSTRACT_ID_ENDPOINT + str(abstract.id))
    authors = []
    detailed_auth = None

    for author_entry in authors_db_entry:
        author = Author(id=author_entry[0], first_name=author_entry[1],
                        last_name=author_entry[2])
        authors.append(author)
        if (auth_id is not None) and (auth_id == author.id):
            detailed_auth = author

    # No author picked for detailed view, pick the first one
    if detailed_auth is None:
        detailed_auth = authors[0]

    competencies_of_abstract_db_entry = access.get_request_from_api(
        COMPETENCIES_BY_ABSTRACT_ID_ENDPOINT + str(id))
    competencies_of_abstract = get_competencies_from_db_entry(
        competencies_of_abstract_db_entry)

    competency_of_author_db_entry = access.get_request_from_api(
        COMPETENCIES_BY_AUTHOR_ID_ENDPOINT
        + str(detailed_auth.id))
    competencies_of_author = get_competencies_from_db_entry(
        competency_of_author_db_entry)

    return render(request, 'abstract.html',
                  {'abstract': abstract, 'detailed_auth': detailed_auth,
                   'authors': authors,
                   'competencies_abs': competencies_of_abstract,
                   'competencies_auth': competencies_of_author})


def get_competencies_from_db_entry(db_entry):
    """Returns a List of competency objects from a db entry

    Args:
        db_entry (json): a JSON Object containing the GET request's answer

    Returns:
        competencies (list): List of competency objects 
    """
    competencies = []
    for competency in db_entry:
        # Depends on order of results in Database Api
        competencies.append(Competency(id=competency[0], name=competency[1]))
    return competencies
