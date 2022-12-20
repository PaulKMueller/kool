import requests

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

class Result:

    id: int
    name: int
    author: dict

class Author:
    def __init__(self, id: int, first_name: str, last_name: str, abstracts: dict):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.abstracts = {}
 
    def add_abstract(self, abstract_id: int, relevancy: float):
        endpoint = main_url + "/abstract_by_id/" + str(abstract_id)
        abstract_db_entry = get_request_from_api(endpoint)
        abstract = Abstract(abstract_db_entry[0], abstract_db_entry[1],
                        abstract_db_entry[2], abstract_db_entry[3],
                        abstract_db_entry[4], abstract_db_entry[5])
        self.abstracts[abstract_id] = (abstract, relevancy)
        print(self.abstracts)

    def get_last_publication_year(self):
        values = list(self.abstracts.values())
        years = [x[0].year for x in values]
        return max(years)

    def get_number_of_publications(self):
        return len(self.abstracts)

class Abstract:
    
    def __init__(self, id: int, year: int, title: str, content: str, doctype: str, institution: str):
        self.id = id
        self.year = year
        self.title = title
        self.content = content
        self.doctype = doctype
        self.institution = institution
