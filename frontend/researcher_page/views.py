"""This module contains the views for the result_page app.
"""

from typing import Optional
from django.shortcuts import render, redirect
from researcher_page.models import Author, Abstract, Competency
import access
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.contrib.auth.decorators import login_required
import json


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
    competencies = []
    author_first_name = None
    author_last_name = None
    searchquery = request.GET.get('q', '')

    if searchquery == "":
        author_id = id
        searched = id
    else:
        author_id = get_author_id(searchquery)
        searched = searchquery

    author_response = get_author_by_id(author_id)

    author_first_name = author_response[0]
    author_last_name = author_response[1]
    if author_id:

        if author_first_name and author_last_name:
            found_id = True

            author_competencies = get_competencies_of_author(author_id)
            for competency in author_competencies:
                competency_id = competency[0]
                ranking = get_ranking_score(author_id, competency_id)

                relevant_abstract_ids = get_relevant_abstract_ids(
                    competency_id, author_id)

                relevant_abstracts = []
                for abstract_id in relevant_abstract_ids:
                    abstract = get_abstract_by_id(abstract_id[0])

                    relevant_abstracts.append(Abstract(abstract[0],
                                              abstract[1],
                                              abstract[2],
                                              abstract[3],
                                              abstract[4],
                                              abstract[5]))

                competencies.append(Competency(competency_id,
                                               competency[1],
                                               competency[2],
                                               ranking,
                                               relevant_abstracts))

            author = Author(id=author_id,
                            first_name=author_first_name,
                            last_name=author_last_name,
                            competencies=competencies)

            competencies = sort_competencies(competencies)

    all_authors = access.get_request_from_api("/all_authors/")
    return render(request, 'researcher.html', {'has_found': found_id,
                                                    'searched': searched,
                                                    'competencies':
                                                        competencies,
                                                    'author': author,
                                                    'all_authors': json.dumps(
                                                        all_authors)}
                  )


def get_author_id(searchquery):
    result = access.get_request_from_api("/author_id_by_full_name/" +
                                         searchquery)
    if not result:
        return None
    return int(result[0])


def get_author_by_id(author_id):
    return access.get_request_from_api("/author_by_id/" +
                                       str(author_id))


def get_competencies_of_author(author_id):
    return access.get_request_from_api(
                    "/competencies_by_author_id/" + str(author_id))


def get_relevant_abstract_ids(competency_id, author_id):
    return access.get_request_from_api(
                    "/abstracts_with_competency_by_author/" +
                    str(competency_id) + "/" + str(author_id))


def get_ranking_score(author_id, competency_id):
    return access.get_request_from_api("/ranking_score/" +
                                       str(author_id) + "/" +
                                       str(competency_id))


def get_abstract_by_id(abstract_id):
    return access.get_request_from_api("/abstract_by_id/" +
                                       str(abstract_id))


def sort_competencies(competencies: list):
    competencies.sort(key=lambda x: x.ranking, reverse=True)
    return competencies


@login_required
def change_status_researcher(request):
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
