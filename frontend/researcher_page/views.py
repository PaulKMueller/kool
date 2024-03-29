"""This module contains the views for the result_page app.
"""

from typing import Optional
import json

from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.contrib.auth.decorators import login_required

import access
from researcher_page.models import Author, Abstract, Competency


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
    author_id = None
    author_first_name = None
    author_last_name = None
    searchquery = request.GET.get('q', '')

    # If ?q=... exists its preferred, else id is used. When no author is
    # found, the user is informed in frontend.
    if searchquery == "":
        author_id = id
        searched = id
    else:
        author_id = get_author_id(searchquery)
        searched = searchquery

    author_response = get_author_by_id(author_id)
    author_first_name = author_response[0]
    author_last_name = author_response[1]

    # The frontend is informed whether the author exists or not
    if author_id and author_first_name and author_last_name:
        found_id = True
        competencies = get_competencies_list(author_id)

        author = Author(id=author_id,
                        first_name=author_first_name,
                        last_name=author_last_name,
                        competencies=competencies)

    all_authors = access.get_request_from_api("/all_authors/")
    return render(request, 'researcher.html', {'has_found': found_id,
                                               'searched': searched,
                                               'author': author,
                                               'all_authors': json.dumps(
                                                        all_authors)})


def get_relevant_abstracts(relevant_abstract_ids: list) -> list[Abstract]:
    """Returns a list of the relevant abstracts that have
    the relevant abstract ids.

    Args:
        relevant_abstract_ids (list): a list of the relevant abstract ids

    Returns:
        list[Abstract]: a list of the abstracts
    """
    relevant_abstracts = []
    for abstract_id in relevant_abstract_ids:
        abstract = get_abstract_by_id(abstract_id[0])

        relevant_abstracts.append(Abstract(abstract[0],
                                           abstract[1],
                                           abstract[2],
                                           abstract[3],
                                           abstract[4],
                                           abstract[5]))
    return relevant_abstracts


def get_competencies_list(author_id: int) -> list[Competency]:
    """Returns a lists of competencies that the author with the author_id has

    Args:
        author_id (int): the id of the author

    Returns:
        list[Competency]: a list of all the competencies the author has
    """
    competencies = []
    author_competencies = get_competencies_of_author(author_id)
    for competency in author_competencies:
        competency_id = competency[0]
        ranking = get_ranking_score(author_id, competency_id)

        relevant_abstracts = get_relevant_abstracts(
                                get_relevant_abstract_ids(
                                    competency_id, author_id))

        competencies.append(Competency(competency_id,
                                       competency[1],
                                       competency[2],
                                       ranking,
                                       relevant_abstracts))
    return sort_competencies(competencies)


def get_author_id(searchquery) -> int:
    """Returns the author id for a given searchquery

    Args:
        searchquery: The searchquery

    Returns:
        int: The author_id
    """
    result = access.get_request_from_api("/author_id_by_full_name/" +
                                         searchquery)
    if not result:
        return None
    return int(result[0])


def get_author_by_id(author_id):
    """Returns the name of the author with the given id

    Args:
        author_id (int): the author id

    Returns:
        tuple: tuple(author_first_name, author_last_name)
    """
    return access.get_request_from_api("/author_by_id/" +
                                       str(author_id))


def get_competencies_of_author(author_id) -> list:
    """Return the competencies of the author with the author id

    Args:
        author_id (int): The id of the author

    Returns:
        list: list[competency_id, competency_name, status]
    """
    return access.get_request_from_api(
                    "/competencies_by_author_id/" + str(author_id))


def get_relevant_abstract_ids(competency_id, author_id) -> list:
    """Returns the relevant abstract ids
    of abstracts by the author with a given relevancy.

    Args:
        competency_id (int): The competency id
        author_id (int): The author id

    Returns:
        list: list[abstract_id]
    """
    return access.get_request_from_api(
                    "/abstracts_with_competency_by_author/" +
                    str(competency_id) + "/" + str(author_id))


def get_ranking_score(author_id, competency_id) -> int:
    """returns the ranking soce of the author and
    the competency.

    Args:
        author_id (int): The author id
        competency_id (int): The competency id

    Returns:
        int: the rnaking score
    """
    return access.get_request_from_api("/ranking_score/" +
                                       str(author_id) + "/" +
                                       str(competency_id))


def get_abstract_by_id(abstract_id) -> list:
    """Returns the abstracts properties of the abstract
    with the given id.

    Args:
        abstract_id (int): The abstract id

    Returns:
        list: List[abstract_id, year, title, content, doctype, institution]
    """
    return access.get_request_from_api("/abstract_by_id/" +
                                       str(abstract_id))


def sort_competencies(competencies: list) -> list:
    """Sorts the list of competencies by the ranking of the competencies.

    Args:
        competencies (list): list[Competency]

    Returns:
        list: list[Competency]
    """
    competencies.sort(key=lambda x: x.ranking, reverse=True)
    return competencies


@login_required
def change_status_researcher(request):
    """Changes the status of
    a competency and a researcher.
    Redirects back to the reseracher page.

    Args:
        request (HttpRequest): The request object.
    """
    if request.method == 'POST':
        competency_id = request.POST['competency_id']
        author_id = request.POST['author_id']
        new_status = request.POST['new_status']
        access.get_request_from_api(
            "/change_status/" + author_id + "/" + competency_id + "/" +
            new_status)
        return redirect('/researcher/' + author_id)
    else:
        return render(request, 'researcher.html')
