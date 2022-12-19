from django.db import models

# Create your models here.


class Abstract:

    def __init__(self, id: int, year: int, title: str, content: str, doctype: str, institution: str):
        self.id = id
        self.year = year
        self.title = title
        self.content = content
        self.doctype = doctype
        self.institution = institution


class Author:
    def __init__(self, id: int, first_name: str, last_name: str):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name


class Competency:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
