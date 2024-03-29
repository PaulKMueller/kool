"""This file contains the functions to create the database."""

from sqlite3 import Error

import adapter

# All available categories
categories = ["Mathematics", "Computer and Informations Sciences",
              "Physical Sciences", "Chemical Sciences",
              "Environmental Sciences",
              "Earth Sciences", "Biological Sciences",
              "Civil Engineering",
              "Electrical Engineering", "Mechanical Engineering",
              "Chemical Engineering", "Materials Engineering",
              "Medical Engineering", "Nano-technology", "Medicine",
              "Health Sciences", "Agriculture, Forestry, and Fisheries",
              "Animal and Dairy Sciences", "Veterinary Sciences",
              "Agricultural Engineering", "Psychology",
              "Economics and Business",
              "Educational Sciences", "Sociology",
              "Law", "Political Sciences",
              "Geography", "Media and Communication",
              "History and Archeology",
              "Languages and Literature", "Philosophy",
              "Ethics and Religion"]

# SQL-Commands to create tables
SQL_CREATE_TABLE_ABSTRACT = """CREATE TABLE IF NOT EXISTS abstract(
                                    abstract_id int IDENTITY(1,1) PRIMARY KEY,
                                    year int,
                                    title text NOT NULL,
                                    content text NOT NULL,
                                    doctype text,
                                    institution text
                                );"""
SQL_CREATE_TABLE_COMPETENCY = """CREATE TABLE IF NOT EXISTS competency(
                                    competency_id integer PRIMARY KEY,
                                    competency_name text NOT NULL
                                );"""
SQL_CREATE_TABLE_AUTHOR = """CREATE TABLE IF NOT EXISTS author(
                                    author_id integer PRIMARY KEY,
                                    first_name text NOT NULL,
                                    last_name text NOT NULL
                                );"""
SQL_CREATE_TABLE_DERIVED_FROM = """CREATE TABLE IF NOT EXISTS derived_from(
                                    competency_id integer,
                                    abstract_id int,
                                    relevancy real,
                                    PRIMARY KEY (abstract_id, competency_id),
                                    FOREIGN KEY (abstract_id)
                                    REFERENCES abstract(abstract_id),
                                    FOREIGN KEY (competency_id)
                                    REFERENCES competency(competency_id)
                                );"""
SQL_CREATE_TABLE_WRITTEN_BY = """CREATE TABLE IF NOT EXISTS written_by(
                                    abstract_id int,
                                    author_id int,
                                    PRIMARY KEY (abstract_id, author_id),
                                    FOREIGN KEY (abstract_id)
                                    REFERENCES abstract(abstract_id),
                                    FOREIGN KEY (author_id)
                                    REFERENCES author(author_id)
                                );"""
SQL_CREATE_TABLE_HAS_COMPETENCY = """CREATE TABLE IF NOT EXISTS has_competency(
                                    author_id int,
                                    competency_id integer,
                                    status text
                                    CHECK(status IN
                                    ('Hidden', 'Unvalidated', 'Validated'))
                                    NOT NULL,
                                    PRIMARY KEY (author_id, competency_id),
                                    FOREIGN KEY (author_id)
                                    REFERENCES author(author_id),
                                    FOREIGN KEY (competency_id)
                                    REFERENCES competency(competency_id)
                                );"""
SQL_CREATE_TABLE_CATEGORY = """CREATE TABLE IF NOT EXISTS category(
                                    category_id integerer PRIMARY KEY,
                                    name varchar(10)
                                );"""
SQL_CREATE_TABLE_CATEGORY = """CREATE TABLE IF NOT EXISTS category(
                                    category_id integer PRIMARY KEY,
                                    name text NOT NULL
                                );"""
SQL_CREATE_TABLE_HAS_CATEGORY = """CREATE TABLE IF NOT EXISTS has_category(
                                    category_id integer,
                                    competency_id integer,
                                    PRIMARY KEY (category_id, competency_id),
                                    FOREIGN KEY (category_id)
                                    REFERENCES category(category_id),
                                    FOREIGN KEY (competency_id)
                                    REFERENCES competency(competency_id)
                                );"""

# Store all created SQL-Commands in a list
sql_commands = [SQL_CREATE_TABLE_ABSTRACT,
                SQL_CREATE_TABLE_COMPETENCY,
                SQL_CREATE_TABLE_AUTHOR,
                SQL_CREATE_TABLE_DERIVED_FROM,
                SQL_CREATE_TABLE_WRITTEN_BY,
                SQL_CREATE_TABLE_HAS_COMPETENCY,
                SQL_CREATE_TABLE_CATEGORY,
                SQL_CREATE_TABLE_HAS_CATEGORY]


def create_table(conn, sql_command: str):
    """Creates a table specified in sql_command.

    Args:
        conn (Connection): Connection to the database
        sql_command (str): SQL-Command in string format
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql_command)
    except Error as error:
        print(error)


def create_database(path_to_db: str):
    """Creates the database and all tables specified in sql_commands.

    Args:
        path_to_db: Path where database should be created
    """
    conn = adapter.create_connection_to(path_to_db)

    if conn is not None:
        for sql_command in sql_commands:
            create_table(conn, sql_command)
    add_categories(conn)


def add_categories(conn):
    """Inserts categories for competencies

    Args:
        conn (Connection): Connection to the database
    """
    for index, category in enumerate(categories):
        adapter.insert_category(conn, category_name=category, category_id=index)
