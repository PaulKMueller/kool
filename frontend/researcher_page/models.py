"""Defines the models used in the result page.
"""

import access


class Author:
    '''Represents an author'''
    def __init__(self, id: int, first_name: str, last_name: str,
                 abstracts: dict, competencies: dict):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.abstracts = abstracts
        self.competencies = competencies


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

    def get_abstracts_with_competency(self, competency_id:int):
        abstracts_with_competency = []
        for abstract in self.abstracts:
            if competency_id in access.get_request_from_api("/competencies_by_abstract_id/{abstract.id}"):
                abstracts_with_competency.append(abstract)
        return abstracts_with_competency
    
    def get_ranking_for_competency_by_id(self, competency_id:int):
        return access.get_request_from_api("/ranking_score/{author_id}/{competency_id}")


class Abstract:
    '''Represents an abstract'''
    def __init__(self, id: int, year: int, title: str, content: str, institution: str):
        self.id = id
        self.year = year
        self.title = title
        self.content = content
        self.institution = institution

class Competency:
    """Represents a competency"""
    def __init__(self, id: int, name: str, competency_status: str):
        """Creates a Competency object

        Args:
            id (int): Competency ID (key in database)
            name (str): Name of the Competency
        """
        self.id = id
        self.name = name
        self.competency_status = competency_status
