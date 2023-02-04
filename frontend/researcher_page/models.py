"""Defines the models used in the researcher page.
"""


class Author:
    """Represents an author entry with its competencies

    Returns:
        Author: author
    """
    def __init__(self, id: int, first_name: str, last_name: str,
                 competencies: dict):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.competencies = competencies

    def get_number_of_publications(self) -> int:
        """Returns number of publications of the given author

        Returns:
            int: number of publications
        """
        abstract_ids = set()
        for competency in self.competencies:
            for abstract in competency.abstracts:
                abstract_ids.add(abstract.id)
        return len(abstract_ids)


class Abstract:
    """Represents an abstract
    """
    def __init__(self, id: int, year: int, title: str, content: str,
                 doctype: str, institution: str):
        self.id = id
        self.year = year
        self.title = title
        self.content = content
        self.doctype = doctype
        self.institution = institution


class Competency:
    """Represents a competency"""
    def __init__(self, id: int, name: str, competency_status: str,
                 ranking: int, abstracts: dict):
        """Creates a Competency object

        Args:
            id (int): Competency ID (key in database)
            name (str): Name of the Competency
            competency_status (str): Status of the Competency
            ranking (int): ranking of the Competency
        """
        self.id = id
        self.name = name
        self.competency_status = competency_status
        self.ranking = ranking
        self.abstracts = abstracts

    def get_last_publication_year(self) -> int:
        """Returns the latest publication year

        Returns:
            int: latest year
        """
        years = [x.year for x in self.abstracts]
        return max(years)

    def get_number_of_publications(self) -> int:
        """Returns number of publications of the given competency

        Returns:
            int: number of abstracts
        """
        return len(self.abstracts)
