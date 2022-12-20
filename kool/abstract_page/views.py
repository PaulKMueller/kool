from django.shortcuts import render
import requests
from abstract_page.models import Abstract, Author, Competency

# Create your views here.

main_url = "http://192.168.123.116:8020"


def get_request_from_api(url):
    for i in range(5):
        try:
            response = requests.get(url)
            return response.json()
        except:
            time.sleep(2)
            continue
    return "connection failed"


def abstract_page(request, id, auth_id=None):
    endpoint = main_url + "/abstract_by_id/" + str(id)
    abstract_db_entry = get_request_from_api(endpoint)
    abstract = Abstract(abstract_db_entry[0], abstract_db_entry[1],
                        abstract_db_entry[2], abstract_db_entry[3],
                        abstract_db_entry[4], abstract_db_entry[5])
    authors_endpoint = main_url + "/author_by_abstract_id/" + str(abstract.id)
    authors_db_entry = get_request_from_api(authors_endpoint)
    authors = []
    print(authors_db_entry)
    detailed_auth = None
    for author_entry in authors_db_entry:
        author = Author(author_entry[0], author_entry[1], author_entry[2])
        authors.append(author)
        if (auth_id is not None) and (auth_id == author.id):
            detailed_auth = author

    # no author found, pick the first one
    if detailed_auth is None:
        detailed_auth = authors[0]

    competencies_abs_endpoint = main_url + \
        "/competencies_by_abstract_id/" + str(id)
    competencies_abs_db_entry = get_request_from_api(competencies_abs_endpoint)
    competencies_abs = []
    for competency in competencies_abs_db_entry:
        competencies_abs.append(Competency(competency[0], competency[1]))

    competency_auth_endpoint = main_url + \
        "/competencies_by_author_id/" + str(detailed_auth.id)
    coompetency_auth_db_entry = get_request_from_api(
        competency_auth_endpoint)
    competencies_auth = []
    for competency in coompetency_auth_db_entry:
        competencies_auth.append(Competency(competency[0], competency[1]))

    return render(request, 'abstract_page.html', {'abstract': abstract,
                                                  'detailed_auth': detailed_auth,
                                                  'authors': authors,
                                                  'competencies_abs':
                                                  competencies_abs,
                                                  'competencies_auth':
                                                  competencies_auth})
