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

def get_author_by_competency_id(competency_id: int):
    """Fetches all authors for a given competency id from the database.

    Args:
        competency_id (int): The id of the competency.

    Returns:s
        list: list[Author]
    """
    authors_db_entry = access.get_request_from_api("/authors_by_competency_id/"
                                                   + str(competency_id))
    authors = {}
    for author_entry in authors_db_entry:
        author_id = author_entry[0]
        author_first_name = author_entry[1]
        author_last_name = author_entry[2]
        abstract_id = author_entry[3]
        relevancy_of_abstract = author_entry[4]
        status = author_entry[5]        
        ranking =  access.get_request_from_api("/ranking_score/" + str(author_id) + "/" + str(competency_id))

        if author_id not in authors:
            authors[author_id] = Author(id=author_id,
                                        first_name=author_first_name,
                                        last_name=author_last_name,
                                        abstracts={},
                                        competency_status=status, 
                                        ranking=ranking)

        authors[author_id].add_abstract(abstract_id, relevancy_of_abstract)
    return authors


def get_competency_name_by_id(competency_id: int):
    """Fetches the name of a competency by its id.

    Args:
        competency_id (int): The id of the competency.

    Returns:
        json: The name of the competency.
    """
    return access.get_request_from_api("/competency_name_by_id/"
                                       + str(competency_id))


def get_competency_id_by_name(competency_name: str):
    """Fetches the id of a competency by its name.

    Args:
        competency_name (str): The name of the competency.

    Returns:
        json: {[id, name]]}
    """
    return access.get_request_from_api("/competency_id_by_name/"
                                       + str(competency_name))


def results(request: HttpRequest, id: Optional[int] = None) -> HttpResponse:
    """Renders the results page.
    If ?q=... exists its preferred, else id is used. When no authors are
    found, the user is informed in frontend.

    Args:
        request (HttpRequest): The request object.
        int: ID of the competency. Defaults to None.

    Returns:
        HttpResponse: The rendered results page.
    """
    found_id = False
    found_authors = False
    searchquery = request.GET.get('q', '')
    authors = {}
    if searchquery == "":
        competency_id = id
        found_id = True
    else:
        competency = searchquery
        result = get_competency_id_by_name(searchquery)
        if result is not None:
            competency_id = result[0]
            found_id = True
    if found_id:
        authors = get_author_by_competency_id(competency_id)
        if len(authors) != 0:
            found_authors = True
            competency = get_competency_name_by_id(competency_id)[0]
    authors = sort_authors(authors)
    all_competencies = access.get_request_from_api("/all_competencies/")

    return render(request, 'result.html', {'has_found': found_authors,
                                           'competency': competency,
                                           'competency_id': competency_id,
                                           'authors': authors,
                                           'all_competencies': json.dumps(
                                            all_competencies)})


@login_required
def change_status(request):
    if request.method == 'POST':
        competency_id = request.POST['competency_id']
        author_id = request.POST['author_id']
        new_status = request.POST['new_status'] 
        access.get_request_from_api("/change_status/" + author_id + "/" + competency_id + "/" + new_status)
        return redirect('/results/' + competency_id)
    else:
        return render(request, 'result.html')

def sort_authors(authors):
    author_list = [(key, value) for key, value in authors.items()]
    sorted_list = sorted(author_list, key=lambda x: x[1].ranking, reverse=True)
    sorted_dict = dict(sorted_list)
    return sorted_dict