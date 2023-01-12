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


class Author:
    '''Represents an author'''
    def __init__(self, id: int, first_name: str, last_name: str):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name


class Competency:
    '''Represents a competency'''
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
