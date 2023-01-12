import access


class Author:
    '''Represents an author'''
    def __init__(self, id: int, first_name: str, last_name: str,
                 abstracts: dict):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.abstracts = abstracts

    def add_abstract(self, abstract_id: int, relevancy: float):
        '''
        Add Abstract to an author

                Parameters:
                        abstract_id (int): id of the given abstract
                        relevancy (float): relevancy of the abstract
        '''
        abstract_db_entry = access.get_request_from_api("/abstract_by_id/"
                                                        + str(abstract_id))
        abstract = Abstract(abstract_db_entry[0], abstract_db_entry[1],
                            abstract_db_entry[2], abstract_db_entry[3],
                            abstract_db_entry[4], abstract_db_entry[5])
        self.abstracts[abstract_id] = (abstract, relevancy)
        print(self.abstracts)

    def get_last_publication_year(self):
        '''
        Returns the latest publication year
                Returns:
                        max (int): latest year
        '''
        values = list(self.abstracts.values())
        years = [x[0].year for x in values]
        return max(years)

    def get_number_of_publications(self):
        '''Returns number of publications of the given author'''
        return len(self.abstracts)


class Abstract:
    '''Represents an abstract'''
    def __init__(self, id: int, year: int, title: str, content: str,
                 doctype: str, institution: str):
        self.id = id
        self.year = year
        self.title = title
        self.content = content
        self.doctype = doctype
        self.institution = institution
