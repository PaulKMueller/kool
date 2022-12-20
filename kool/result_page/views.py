from django.shortcuts import render
import pandas as pd
import requests
from result_page.models import Author 

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

def getAuthorByCompId(competency_id):
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

def results(request, id = None):
    searchquery = request.GET.get('q', '')
    print(searchquery)
    authors = getAuthorByCompId(id)
    
    return render(request, 'result_page.html', {'authors': authors})
