class Abstract:
    """Represents an abstract"""
    def __init__(self, id: int, year: int, title: str, content: str,
                 doctype: str, institution: str):
        """Creates an Abstract object

        Args:
            id (int): Abstract ID (key in database)
            year (int): Release Year of the Abstract
            title (str): Title of the Abstract
            content (str): Content of the Abstract
            doctype (str): Doctype of the Abstract
            institution (str): Institution which released the Abstract
        """
        self.id = id
        self.year = year
        self.title = title
        self.content = content
        self.doctype = doctype
        self.institution = institution


class Author:
    """Represents an author"""
    def __init__(self, id: int, first_name: str, last_name: str):
        """Creates an Author object

        Args:
            id (int): Author ID (key in database)
            first_name (str): First Name of the Author
            last_name (str): Last Name of the Author 
        """
        self.id = id
        self.first_name = first_name
        self.last_name = last_name


class Competency:
    """Represents a competency"""
    def __init__(self, id: int, name: str):
        """Creates a Competency object

        Args:
            id (int): Competency ID (key in database)
            name (str): Name of the Competency
        """
        self.id = id
        self.name = name
