from django.shortcuts import render
import requests
from abstract_page.models import Abstract, Author, Competency
import json
# Create your views here.
import access

def abstract_page(request, id, auth_id=None):
    abstract_db_entry = access.get_request_from_api("/abstract_by_id/" + str(id))
    abstract = Abstract(abstract_db_entry[0], abstract_db_entry[1],
                        abstract_db_entry[2], abstract_db_entry[3],
                        abstract_db_entry[4], abstract_db_entry[5])
    authors_db_entry = access.get_request_from_api("/author_by_abstract_id/" + str(abstract.id))
    authors = []
    detailed_auth = None
    for author_entry in authors_db_entry:
        author = Author(author_entry[0], author_entry[1], author_entry[2])
        authors.append(author)
        if (auth_id is not None) and (auth_id == author.id):
            detailed_auth = author

    # no author found, pick the first one
    if detailed_auth is None:
        detailed_auth = authors[0]
    competencies_abs_db_entry = access.get_request_from_api("/competencies_by_abstract_id/" + str(id))
    competencies_abs = []
    for competency in competencies_abs_db_entry:
        competencies_abs.append(Competency(competency[0], competency[1]))
    coompetency_auth_db_entry = access.get_request_from_api("/competencies_by_author_id/" + str(detailed_auth.id))
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
