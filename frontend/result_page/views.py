from django.shortcuts import render
import pandas as pd
from result_page.models import Author
import json
import access


def get_author_by_competency_id(competency_id):
    authors_db_entry = access.get_request_from_api("/authors_by_competency_id/"
                                                   + str(competency_id))
    authors = {}
    for author_entry in authors_db_entry:
        author_id = author_entry[0]
        author_first_name = author_entry[1]
        author_last_name = author_entry[2]
        abstract_id = author_entry[3]
        relevancy_of_abstract = author_entry[4]
        ranking =  access.get_request_from_api("/ranking_score/" + str(author_id) + "/" + str(competency_id))

        if author_id not in authors:
            authors[author_id] = Author(author_id, author_first_name,
                                        author_last_name, {}, ranking)

        authors[author_id].add_abstract(abstract_id, relevancy_of_abstract)
    return authors


def get_competency_name_by_id(competency_id):
    return access.get_request_from_api("/competency_name_by_id/"
                                       + str(competency_id))


def get_competency_id_by_name(competency_name):
    return access.get_request_from_api("/competency_id_by_name/"
                                       + str(competency_name))

    

def results(request, id=None):
    """if ?q=... exists its preferred, else id is used. When no authors found
    user is informed in frontend"""
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
    return render(request, 'result_page.html', {'has_found': found_authors,
                  'competency': competency,
                  'authors': authors,
                  'all_competencies': json.dumps(all_competencies)})


def sort_authors(authors):
    author_list = [(key, value) for key, value in authors.items()]
    sorted_list = sorted(author_list, key=lambda x: x[1].ranking, reverse=True)
    sorted_dict = dict(sorted_list)
    return sorted_dict