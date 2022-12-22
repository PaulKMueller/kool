from django.shortcuts import render
import pandas as pd
import requests
from result_page.models import Author 
import json

resultsdict = []

csvreader = pd.read_csv('/workspaces/kool/kool/firsttest.csv', 
                        encoding='UTF-8',
                        header=None)

main_url = "http://192.168.123.116:8020"

# iterating through csv file using pandas
for expert, trustworthiness in zip(csvreader[0], csvreader[1]):
    resultsdict.append([expert, trustworthiness])

def get_request_from_api(url):
    for i in range(5):
        try:
            response = requests.get(url)
            return response.json()
        except:
            time.sleep(2)
            continue
    return "connection failed"

def get_author_by_competency_id(competency_id):
    request_url = main_url + "/authors_by_competency_id/" + str(competency_id)
    authors_db_entry = get_request_from_api(request_url)
    authors = {}
    for author_entry in authors_db_entry:
        author_id = author_entry[0]
        author_first_name = author_entry[1]
        author_last_name = author_entry[2]
        abstract_id = author_entry[3]
        relevancy = author_entry[4]

        if author_id not in authors:
            authors[author_id] = Author(author_id, author_first_name, author_last_name, {})
    
        authors[author_id].add_abstract(abstract_id, relevancy)
    return authors

def get_competency_name_by_id(competency_id):
    requests_url = main_url + "/competency_name_by_id/" + str(competency_id)
    return get_request_from_api(requests_url)

def get_competency_id_by_name(competency_name):
    requests_url = main_url + "/competency_id_by_name/" + str(competency_name)
    return get_request_from_api(requests_url)


def results(request, id = None):
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

    req_all_comp = main_url + "/all_competencies/"
    all_competencies = get_request_from_api(req_all_comp)

    return render(request, 'result_page.html', {'has_found': found_authors,
     'competency': competency,
      'authors': authors,
      'all_competencies': json.dumps(all_competencies)})
