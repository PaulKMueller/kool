"""Provides functionality to interact with the database."""

import sqlite3
from sqlite3 import Error
import yaml
import numpy as np

with open("database_api/db_creation/db_config.yml",
          "r", encoding='utf-8') as ymlfile:
    cfg = yaml.safe_load(ymlfile)

# Path to existing database or where the database should be created
PATH_TO_DB = cfg["paths"]["path_to_db"]


def create_connection():
    """Creates a connection to the database or creates a
    new database if it does not existent

    Returns:
        Connection: Connection to database
    """
    conn = None
    try:
        conn = sqlite3.connect(PATH_TO_DB)
    except Error as error:
        print(error)

    return conn


def insert_abstract(conn, db_entry_abstract):
    """Inserts an abstract into the database.

    Args:
        conn (Connection): Connection to the database
        db_entry_abstract (list): List of the abstract's attributes
    """
    sql_command = ("INSERT INTO abstract(abstract_id, year, title, "
                   "content, doctype, institution) VALUES(?,?,?,?,?,?)")
    cursor = conn.cursor()
    cursor.execute(sql_command, db_entry_abstract)
    conn.commit()


def insert_written_by(conn, abstract_id, author_id):
    """Inserts an entry into the written_by relation in the database.

    Args:
        conn (Connection): Connection to the database
        abstract_id (int): Id of the abstract
        author_id (int): Id of the author
    """
    sql_command = ("INSERT INTO written_by(abstract_id, "
                   "author_id) VALUES(?,?)")
    cursor = conn.cursor()
    cursor.execute(sql_command, (abstract_id, author_id))
    conn.commit()


def insert_has_competency(conn, author_id, competency_id, status):
    """Inserts an entry into the has_competency relation in the database.

    Args:
        conn (Connection): Connection to the database
        author_id (int): Id of the author
        competency_id (int): Id of the competency
        status (str): Status of the competency from {denied, neutral, accepted}
    """
    sql_command = ("INSERT OR IGNORE INTO has_competency"
                   "(author_id, competency_id, status) VALUES(?,?,?)")
    cursor = conn.cursor()
    cursor.execute(sql_command, (author_id, competency_id, status))
    conn.commit()


def insert_derived_from(conn, competency_id, abstract_id, relevancy):
    """Inserts an entry into the derived_from relation in the database.

    Args:
        conn (Connection): Connection to the database
        competency_id (int): Id of the competency
        abstract_id (int): Id of the abstract
        relevancy (float): Relevancy of the competency to the abstract
    """
    sql_command = ("INSERT INTO derived_from(competency_id, "
                   "abstract_id, relevancy) VALUES(?,?,?)")
    cursor = conn.cursor()
    cursor.execute(sql_command, (competency_id, abstract_id, relevancy))
    conn.commit()


def insert_category(conn, category_id, category_name):
    """Inserts an entry into the category relation in the database.

    Args:
        conn (Connection): Connection to the database
        category_id (int): Id of the category
        category_name (str): Name of the category
    """
    sql_command = """INSERT INTO category(category_id, name) VALUES(?,?)"""
    cursor = conn.cursor()
    cursor.execute(sql_command, (category_id, category_name))
    conn.commit()


def insert_has_category(conn, category_id, competency_id):
    """Inserts an entry into the has_category relation in the database.

    Args:
        conn (Connection): Connection to the database
        category_id (int): Id of the category
        competency_id (int): Id of the competency
    """
    sql_command = """INSERT INTO has_category(category_id, competency_id)
                    VALUES(?,?)"""
    cursor = conn.cursor()
    cursor.execute(sql_command, (category_id, competency_id))
    conn.commit()


def get_author_id_by_name(conn, first_name, last_name):
    """Returns the id of an author by its name or creates an id if the author's
    id has not been created yet.

    Args:
        conn (Connection): Connection to the database
        first_name (str): First name of the author
        last_name (str): Last name of the author

    Returns:
        int: Id of the author
    """
    sql_get_author_id = """SELECT author_id
                           FROM author
                           WHERE first_name = ? AND last_name = ?;"""
    sql_insert_author = """INSERT INTO author(first_name, last_name)
    VALUES(?,?)"""
    cursor = conn.cursor()
    cursor.execute(sql_get_author_id, (first_name, last_name))
    result = cursor.fetchone()
    if result is None:
        # author not in db -> needs to be created
        author_id = cursor.execute(sql_insert_author,
                                   (first_name, last_name)).lastrowid
    else:
        # fetchone returns tuple, we want only the author_id
        author_id = result[0]

    conn.commit()
    return author_id


def add_category(conn, competency_name):
    """Adds an entry to the category relation in the database.

    Args:
        conn (Connection): Connection to the database
        competency_name (str): Name of the competency

    Returns:
        int: Id of the competency
    """
    sql_get_competency_id = """SELECT competency_id
                               FROM competency
                               WHERE competency_name = ?"""
    sql_insert_competency = """INSERT INTO competency(competency_name)
                               VALUES(?)"""
    cursor = conn.cursor()
    cursor.execute(sql_get_competency_id, (competency_name,))
    result = cursor.fetchone()
    if result is None:
        # Competency not in db -> needs to be created
        competency_id = cursor.execute(sql_insert_competency,
                                       (competency_name,)).lastrowid
    else:
        # Fetchone returns tuple, we want only the author_id
        competency_id = result[0]

    conn.commit
    return competency_id


def get_all_categories(conn):
    """Returns all entries in the category relation in the database.

    Args:
        conn (Connection): Connection to the database

    Returns:
        list: List[category_id, name]
    """
    sql_get_categories = """SELECT * FROM category;"""
    cursor = conn.cursor()
    cursor.execute(sql_get_categories)
    result = cursor.fetchall()
    if result is None:
        return """Something went wrong. Result for the query to fetch
    all entries of the category relation is None."""
    conn.commit()
    return result


def get_all_competencies(conn):
    """Returns all entries in the competency relation in the database.

    Args:
        conn (Connection): Connection to the database

    Returns:
        list: List[competency_id, competency_name, relevancy]
    """
    sql_get_categories = """SELECT * FROM competency;"""
    cursor = conn.cursor()
    cursor.execute(sql_get_categories)
    result = cursor.fetchall()
    if result is None:
        return 'Something went wrong.'
    conn.commit()
    return result


def get_or_generate_competency_id_by_name(conn, competency_name):
    '''Returns competency_id for a given name and inserts if name not yet in db'''
    """Returns the id of a competency by its name or creates an id if the
    competency's id has not been created yet.

    Args:
        conn (Connection): Connection to the database
        competency_name (str): Name of the competency

    Returns:
        int: Id of the competency
    """
    sql_get_competency_id = """SELECT competency_id
                               FROM competency
                               WHERE competency_name = ?"""
    sql_insert_competency = """INSERT INTO competency(competency_name)
                               VALUES(?)"""
    cursor = conn.cursor()
    cursor.execute(sql_get_competency_id, (competency_name,))
    result = cursor.fetchone()
    if result is None:
        # competency not in db -> needs to be created
        competency_id = cursor.execute(sql_insert_competency,
                                       (competency_name,)).lastrowid
    else:

        competency_id = result[0]

    conn.commit
    return competency_id

def get_competency_id_by_name(conn, competency_id):
    '''returns competency id for a given name'''
    sql_get_competency_id = """SELECT competency_id 
                            FROM competency
                            WHERE competency_name = ?"""
    c = conn.cursor()
    c.execute(sql_get_competency_id, (competency_id,))
    competeny_name = c.fetchone()
    conn.commit
    return competeny_name 

def get_competency_name_by_id(conn, competency_id):
    """Returns the name of a competency by its id.

    Args:
        conn (Connection): Connection to the database
        competency_id (int): Id of the competency

    Returns:
        str: Name of the competency
    """
    sql_get_competency_id = """SELECT competency_name 
                            FROM competency
                            WHERE competency_id = ?"""
    cursor = conn.cursor()
    cursor.execute(sql_get_competency_id, (competency_id,))
    competeny_name = cursor.fetchone()
    return competeny_name


def get_category_name_by_id(conn, category_id):
    """Returns the name of a category by its id.

    Args:
        conn (Connection): Connection to the database
        category_id (int): Id of the category

    Returns:
        str: Name of the category
    """
    sql_command = """SELECT name
                     FROM category
                     WHERE category_id = ?"""
    cursor = conn.cursor()
    cursor.execute(sql_command, (category_id,))
    category_name = cursor.fetchone()
    print("-------------------")
    print(category_name)
    return category_name


def get_competencies_by_category(conn, category_name):
    """Returns all competencies for a given category.

    Args:
        conn (Connection): Connection to the database
        category (str): Name of the category

    Returns:
        list: List[competency_name]
    """
    sql_get_competencies = """SELECT comp.competency_name FROM competency comp
                              JOIN has_category hc ON comp.competency_id
                              = hc.competency_id JOIN category cat ON
                              hc.category_id = cat.category_id
                              WHERE cat.name = ?;"""
    cursor = conn.cursor()
    cursor.execute(sql_get_competencies, (category_name,))
    result = cursor.fetchall()
    if result is None:
        return 'There are no competencies for this category.'
    conn.commit()
    return result


def get_competencies_by_category_id(conn, category_id):
    """Returns all competencies for a given category.

    Args:
        conn (Connection): Connection to the database
        category_id (int): Id of the category

    Returns:
        list: List[competency_id, competency_name]
    """
    sql_get_competencies = """SELECT comp.competency_id, comp.competency_name
                              FROM competency comp
                              JOIN has_category hc ON comp.competency_id
                              = hc.competency_id
                              WHERE hc.category_id = ?;"""
    cursor = conn.cursor()
    cursor.execute(sql_get_competencies, (category_id,))
    result = cursor.fetchall()
    print(result)
    if result is None:
        return 'There are no competencies for this category.'
    conn.commit()
    return result


def get_competencies_by_author_id(conn, author_id):
    """Returns all competencies for a given author.

    Args:
        conn (Connection): Connection to the database
        author_id (int): Id of the author

    Returns:
        list: List[competency_id, competency_name, status]
    """
    sql_get_competencies = """SELECT hc.competency_id, comp.competency_name,
                              hc.status FROM has_competency hc
                              JOIN competency comp ON
                              comp.competency_id = hc.competency_id
                              WHERE hc.author_id = ?;"""
    cursor = conn.cursor()
    cursor.execute(sql_get_competencies, (author_id,))
    result = cursor.fetchall()
    print(result)
    if result is None:
        return 'There are no competencies for this author.'
    conn.commit()
    return result


def get_competencies_by_abstract_id(conn, abstract_id):
    """Returns all competencies for a given abstract.

    Args:
        conn (Connection): Connection to the database
        abstract_id (int): Id of the abstract

    Returns:
        list: List[competency_id, competency_name, relevancy]
    """
    sql_get_competencies = """SELECT df.competency_id, comp.competency_name,
                              df.relevancy FROM derived_from df
                              JOIN competency comp ON
                              comp.competency_id = df.competency_id
                              WHERE df.abstract_id = ?;"""
    cursor = conn.cursor()
    cursor.execute(sql_get_competencies, (abstract_id,))
    result = cursor.fetchall()
    print(result)
    if result is None:
        return 'There are no competencies for this author.'
    conn.commit()
    return result


def get_abstract_by_id(conn, abstract_id):
    """Returns an abstract (consisting of all its attributes) by its id.

    Args:
        conn (Connection): Connection to the database
        abstract_id (int): Id of the abstract

    Returns:
        list: List[abstract_id, year, title, content, doctype, institution]
    """
    sql_get_abstract = """SELECT * FROM abstract
                          WHERE abstract_id = ?;"""
    cursor = conn.cursor()
    cursor.execute(sql_get_abstract, (abstract_id,))
    result = cursor.fetchone()
    if result is None:
        return 'There exists no abstract with the given id.'
    conn.commit()
    return result


def get_authors_by_abstract(conn, abstract_id):
    """Returns all authors of a given abstract.

    Args:
        conn (Connection): Connection to the database
        abstract_id (int): Id of the abstract

    Returns:
        list: List[author_id, first_name, last_name]
    """
    # TODO Search for usages of this funtion and replace
    # them with get_authors_by_abstract_id
    sql_get_abstract = """SELECT auth.author_id, auth.first_name,
                          auth.last_name FROM abstract abs
                          JOIN written_by wb
                          ON wb.abstract_id = abs.abstract_id
                          JOIN author auth ON wb.author_id = auth.author_id
                          WHERE abs.abstract_id = ?;"""
    cursor = conn.cursor()
    cursor.execute(sql_get_abstract, (abstract_id,))
    result = cursor.fetchall()
    if result is None:
        return 'There exists no author with the given abstract id.'
    conn.commit()
    return result


def get_authors_with_competency(conn, competency):
    """Returns all authors with a given competency and the status of the
    competency.

    Args:
        conn (Connection): Connection to the database
        competency_name (str): Name of the competency

    Returns:
        list: List[author_id, first_name, last_name, relevancy, status]
    """
    sql_get_authors = """SELECT auth.author_id, auth.first_name, auth.last_name, 
                         df.relevancy, hc.status 
                         FROM author auth JOIN has_competency hc 
                         ON auth.author_id = hc.author_id JOIN competency comp 
                         ON hc.competency_id = comp.competency_id JOIN
                         derived_from df ON comp.competency_id = df.competency_id
                         WHERE comp.competency_name = ?;"""
    c = conn.cursor()
    c.execute(sql_get_authors, (competency,))
    result = c.fetchall()
    if result is None:
        return 'There are no people with this competency.'
    conn.commit()
    return result 

def get_authors_by_competency_id(conn, competency_id):
    'Returns all authors with the given competency as well as relevency and status'
    sql_get_authors = """SELECT auth.author_id, auth.first_name, auth.last_name, df.abstract_id, df.relevancy
                         FROM author auth JOIN has_competency hc 
                         ON auth.author_id = hc.author_id 
                         LEFT JOIN derived_from df ON df.competency_id = hc.competency_id
                         JOIN written_by wb ON wb.author_id = auth.author_id AND wb.abstract_id = df.abstract_id
                         WHERE hc.competency_id= ?;"""
    c = conn.cursor()
    c.execute(sql_get_authors, (competency_id,))
    result = c.fetchall()
    if result is None:
        return 'There are no people with this competency.'
    conn.commit()
    print(c.description)
    return result 

def get_abstracts_by_author(conn, author_first_name, author_last_name):
    """Returns all abstracts of a given author.

    Args:
        conn (Connectino): Connection to the database
        author_first_name (str): First name of the author
        author_last_name (str): Last name of the author

    Returns:
        list: List[abstract_id, year, title, content, institution]
    """
    sql_get_abstracts = """SELECT abs.abstract_id, abs.year, abs.title,
                           abs.content, abs.institution
                           FROM abstract abs JOIN
                           written_by wb ON abs.abstract_id
                           = wb.abstract_id JOIN author auth
                           ON wb.author_id = auth.author_id
                           WHERE auth.first_name = ? AND
                           auth.last_name = ?;"""

    cursor = conn.cursor()
    cursor.execute(sql_get_abstracts, (author_first_name, author_last_name))
    result = cursor.fetchall()
    if result is None:
        return 'There are no abstracts from this author.'
    conn.commit()
    return result


def get_abstracts_with_competency(conn, competency_id, author_id):
    """Returns all abstracts_ids of the abstracts that proof that an author has
    a given competency.

    Args:
        conn (Connection): Connection to the database
        competency_id (int): Id of the competency
        author_id (int): Id of the author

    Returns:
        list: List[abstract_id]
    """
    sql_get_abstracts_with_competency = """SELECT wb.abstract_id
                                           FROM derived_from df
                                           JOIN written_by wb
                                           ON df.abstract_id = wb.abstract_id
                                           WHERE competency_id = ?
                                           AND author_id = ?
                                           """
    cursor = conn.cursor()
    cursor.execute(sql_get_abstracts_with_competency,
                   (competency_id, author_id))
    abstracts = cursor.fetchall()
    conn.commit()
    return abstracts


# def get_relevancy(conn, author_id, competency_id):
    # """Returns the relevancy of a given competency for a given author.

    # Args:
    #     conn (Connection): Connection to the database
    #     author_id (int): Id of the author
    #     competency_id (int): Id of the competency

    # Returns:
    #     _type_: _description_
    # """

    # # TODO Funktionalität überarbeiten, macht ziemlich sicher
    # # nicht das was sie soll. Außerdem umbennenen, nicht get_relevancy,
    # da der Begriff "relevancy" schon in anderem Kontext verwendet wird.
    # FAILURE_DEFAULT = -1
    # sql_get_relevancies = """SELECT relevancy
    #                          FROM derived_from df JOIN
    #                          written_by wb ON df.abstract_id = wb.abstract_id
    #                          WHERE competency_id = ? AND
    #                          author_id = ?
    #                         """
    # cursor = conn.cursor()
    # cursor.execute(sql_get_relevancies, (competency_id, author_id))
    # relevancies = cursor.fetchall()
    # if relevancies is None:
    #     return FAILURE_DEFAULT
    # conn.commit()

    # author_first_name, author_last_name = get_author_name(conn, author_id)
    # if author_first_name is None and author_last_name and None:
    #     return FAILURE_DEFAULT

    # abstracts_by_author = get_abstracts_by_author(conn, author_first_name,
    #                                               author_last_name)
    # if abstracts_by_author == 'There are no abstracts from this author.':
    #     return FAILURE_DEFAULT
    # total_abstracts = len(abstracts_by_author)

    # abstracts_with_competency = get_abstracts_with_competency(conn,
    #                                                           competency_id,
    #                                                           author_id)
    # if abstracts_with_competency == []:
    #     return FAILURE_DEFAULT
    # amount_abstracts_with_competency = len(abstracts_with_competency)

    #  proportion_competency = amount_abstracts_with_competency /
    # total_abstracts

    # max = np.amax(relevancies)

    # relevancy = np.mean([max, proportion_competency])
    # # arbitrary calculation of relevancy
    # # (mean of highest relevancy and proportion)
    # return relevancy


def get_author_name(conn, author_id):
    """Returns the name of an author.

    Args:
        conn (Connection): Connection to the database
        author_id (int): Id of the author

    Returns:
        list: [first_name, last_name]
    """
    sql_get_author_name = """SELECT first_name, last_name
                             FROM author
                             WHERE author_id = ?
                            """
    cursor = conn.cursor()
    cursor.execute(sql_get_author_name, [author_id])

    author = cursor.fetchone()
    if author is None:
        return None, None
    conn.commit()
    return author


def get_all_authors(conn):
    """Returns all entries in the author relation in the database.

    Args:
        conn (Connection): Connection to the database

    Returns:
        list: List[author_id, first_name, last_name]
    """
    sql_get_authors = """SELECT * FROM author;"""
    cursor = conn.cursor()
    cursor.execute(sql_get_authors)
    result = cursor.fetchall()
    if result is None:
        return ("Something went wrong. Result for the query to fetch",
                "all entries of the author relation is None.")
    conn.commit()
    return result