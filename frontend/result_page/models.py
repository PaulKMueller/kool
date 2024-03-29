"""Defines the models used in the result page.
"""

import access


class Author:
    """Represents an author

    Returns:
        Author: Author
    """
    def __init__(self, id: int, first_name: str, last_name: str,
                 abstracts: dict, competency_status: str, ranking: float):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.abstracts = abstracts
        self.competency_status = competency_status
        self.ranking = ranking

    def add_abstract(self, abstract_id: int, relevancy: float):
        """Add Abstract to an author

        Args:
            abstract_id (int): id of the given abstract
            relevancy (float): relevancy of the abstract
        """
        abstract_db_entry = access.get_request_from_api("/abstract_by_id/"
                                                        + str(abstract_id))
        abstract = Abstract(id=abstract_db_entry[0],
                            year=abstract_db_entry[1],
                            title=abstract_db_entry[2],
                            content=abstract_db_entry[3],
                            doctype=abstract_db_entry[4],
                            institution=abstract_db_entry[5])
        self.abstracts[abstract_id] = (abstract, relevancy)

    def get_last_publication_year(self) -> int:
        """Returns the latest publication year

        Returns:
            int: latest year
        """
        values = list(self.abstracts.values())
        years = [x[0].year for x in values]
        return max(years)

    def get_number_of_publications(self) -> int:
        """Returns number of publications of the given author

        Returns:
            int: number of publications
        """
        return len(self.abstracts)


class Abstract:
    """Represents an abstract'
    """
    def __init__(self, id: int, year: int, title: str, content: str,
                 doctype: str, institution: str):
        self.id = id
        self.year = year
        self.title = title
        self.content = content
        self.doctype = doctype
        self.institution = institution
