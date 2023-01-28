"""
Provides functionality to interact with the database.
"""

import sqlite3
from sqlite3 import Error
import os
import numpy as np


# Path to existing database or where the database should be created
PATH_TO_DB = os.environ.get('PATH_TO_DB')


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


def insert_written_by(conn, abstract_id: int, author_id: int):
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


def insert_has_competency(conn, author_id: int,
                          competency_id: int, status: str):
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


def insert_derived_from(conn, competency_id: int,
                        abstract_id: int, relevancy: float):
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


def insert_category(conn, category_id: int, category_name: str):
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


def insert_has_category(conn, category_id: int, competency_id: int):
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


def get_author_id_by_name(conn, first_name: str, last_name: str) -> int:
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


def add_category(conn, competency_name: str) -> int:
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

    conn.commit()
    return competency_id


def get_all_categories(conn) -> list[int, str]:
    """Returns all entries in the category relation in the database.

    Args:
        conn (Connection): Connection to the database

    Returns:
        list: list[category_id, name]
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


def get_all_competencies(conn) -> list[int, str]:
    """Returns all entries in the competency relation in the database.

    Args:
        conn (Connection): Connection to the database

    Returns:
        list: list[competency_id, competency_name]
    """
    sql_get_categories = """SELECT * FROM competency;"""
    cursor = conn.cursor()
    cursor.execute(sql_get_categories)
    result = cursor.fetchall()
    if result is None:
        return 'Something went wrong.'
    conn.commit()
    return result


def get_or_generate_competency_id_by_name(conn, competency_name: str) -> int:
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

    conn.commit()
    return competency_id


def get_competency_id_by_name(conn, competency_id) -> int:
    """Returns the id of a competency by its name.

    Args:
        conn (Connection): Connection to the database
        competency_id (int): Id of the competency

    Returns:
        int: Id of the competency
    """
    sql_get_competency_id = """SELECT competency_id
                            FROM competency
                            WHERE competency_name = ?"""
    cursor = conn.cursor()
    cursor.execute(sql_get_competency_id, (competency_id,))
    competency_id = cursor.fetchone()
    conn.commit()
    return competency_id


def get_competency_name_by_id(conn, competency_id) -> str:
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


def get_category_name_by_id(conn, category_id: int) -> str:
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
    return category_name


def get_competencies_by_category(conn, category_name: str) -> list[int, str]:
    """Returns all competencies for a given category.

    Args:
        conn (Connection): Connection to the database
        category (str): Name of the category

    Returns:
        list: list[competency_name]
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


def get_competencies_by_category_id(conn, category_id: int) -> list[int, str]:
    """Returns all competencies for a given category.

    Args:
        conn (Connection): Connection to the database
        category_id (int): Id of the category

    Returns:
        list: list[competency_id, competency_name]
    """
    sql_get_competencies = """SELECT comp.competency_id, comp.competency_name
                              FROM competency comp
                              JOIN has_category hc ON comp.competency_id
                              = hc.competency_id
                              WHERE hc.category_id = ?;"""
    cursor = conn.cursor()
    cursor.execute(sql_get_competencies, (category_id,))
    result = cursor.fetchall()
    if result is None:
        return 'There are no competencies for this category.'
    conn.commit()
    return result


def get_competencies_by_author_id(conn, author_id: int) -> list[int, str]:
    """Returns all competencies for a given author.

    Args:
        conn (Connection): Connection to the database
        author_id (int): Id of the author

    Returns:
        list: list[competency_id, competency_name, status]
    """
    sql_get_competencies = """SELECT hc.competency_id, comp.competency_name,
                              hc.status FROM has_competency hc
                              JOIN competency comp ON
                              comp.competency_id = hc.competency_id
                              WHERE hc.author_id = ?;"""
    cursor = conn.cursor()
    cursor.execute(sql_get_competencies, (author_id,))
    result = cursor.fetchall()
    if result is None:
        return 'There are no competencies for this author.'
    conn.commit()
    return result


def get_competencies_by_abstract_id(conn, abstract_id: int) -> list[int, str]:
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
    if result is None:
        return 'There are no competencies for this author.'
    conn.commit()
    return result


def get_abstract_by_id(conn,
                       abstract_id: int) -> list[int, int, str, str, str, str]:
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


def get_authors_by_abstract(conn, abstract_id: int) -> list[int, str, str]:
    """Returns all authors of a given abstract.

    Args:
        conn (Connection): Connection to the database
        abstract_id (int): Id of the abstract

    Returns:
        list: List[author_id, first_name, last_name]
    """
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


def get_authors_with_competency(conn,
                                competency: str) -> list[
                                    int, str, str, int, str]:
    """Returns all authors with a given competency and the status of the
    competency.

    Args:
        conn (Connection): Connection to the database
        competency_name (str): Name of the competency

    Returns:
        list: list[author_id, first_name, last_name, relevancy, status]
    """
    sql_get_authors = """SELECT auth.author_id, auth.first_name,
                         auth.last_name,
                         df.relevancy, hc.status
                         FROM author auth JOIN has_competency hc
                         ON auth.author_id = hc.author_id JOIN competency comp
                         ON hc.competency_id = comp.competency_id JOIN
                         derived_from df
                         ON comp.competency_id = df.competency_id
                         WHERE comp.competency_name = ?;"""
    cursor = conn.cursor()
    cursor.execute(sql_get_authors, (competency,))
    result = cursor.fetchall()
    if result is None:
        return 'There are no people with this competency.'
    conn.commit()
    return result


def get_authors_by_competency_id(conn,
                                 competency_id: int) -> list[
                                    int, str, str, float, str]:
    """Returns all authors with a given competency with its
    relevancy and status.

    Args:
        conn (Connection): Connection to the database
        competency_id (int): Id of the competency

    Returns:
        list: List[author_id, first_name, last_name, abstract_id, relevancy, status]
    """
    sql_get_authors = """SELECT auth.author_id, auth.first_name,
                         auth.last_name, df.abstract_id, df.relevancy, status
                         FROM author auth JOIN has_competency hc
                         ON auth.author_id = hc.author_id
                         LEFT JOIN derived_from df
                         ON df.competency_id = hc.competency_id
                         JOIN written_by wb ON wb.author_id = auth.author_id
                         AND wb.abstract_id = df.abstract_id
                         WHERE hc.competency_id= ?;"""
    cursor = conn.cursor()
    cursor.execute(sql_get_authors, (competency_id,))
    result = cursor.fetchall()
    if result is None:
        return 'There are no people with this competency.'
    conn.commit()
    return result


def get_abstracts_by_author(conn, author_first_name: str,
                            author_last_name: str) -> list[
                                int, int, str, str, str]:
    """Returns all abstracts of a given author.

    Args:
        conn (Connectino): Connection to the database
        author_first_name (str): First name of the author
        author_last_name (str): Last name of the author

    Returns:
        list: list[abstract_id, year, title, content, institution]
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


def get_abstracts_with_competency(conn, competency_id: int,
                                  author_id: int) -> list[int]:
    """Returns all abstracts_ids of the abstracts that proof that an author has
    a given competency.

    Args:
        conn (Connection): Connection to the database
        competency_id (int): Id of the competency
        author_id (int): Id of the author

    Returns:
        list: list[abstract_id]
    """
    sql_get_abstracts_with_competency = """SELECT wb.abstract_id
                                           FROM derived_from df
                                           JOIN written_by wb
                                           ON df.abstract_id = wb.abstract_id
                                           WHERE df.competency_id = ?
                                           AND wb.author_id = ?
                                           """
    cursor = conn.cursor()
    cursor.execute(sql_get_abstracts_with_competency,
                   (competency_id, author_id))
    abstracts = cursor.fetchall()
    conn.commit()
    return abstracts


def get_ranking_score(conn, author_id, competency_id) -> int:
    """Returns the ranking score of a given competency for a given author.

    Args:
        conn (Connection): Connection to the database
        author_id (int): Id of the author
        competency_id (int): Id of the competency

    Returns:
        _type_: _description_
    """
    FAILURE_DEFAULT = 0
    sql_get_relevancies = """SELECT relevancy
                             FROM derived_from df JOIN
                             written_by wb ON df.abstract_id = wb.abstract_id
                             WHERE competency_id = ? AND
                             author_id = ?
                            """
    cursor = conn.cursor()
    cursor.execute(sql_get_relevancies, (competency_id, author_id))
    relevancies = cursor.fetchall()
    if relevancies is None or -1 in relevancies:    # no relevancies or dummy relevancies
        return FAILURE_DEFAULT
    conn.commit()

    author_first_name, author_last_name = get_author_name(conn, author_id)
    if author_first_name is None and author_last_name is None:
        return FAILURE_DEFAULT

    abstracts_by_author = get_abstracts_by_author(conn, author_first_name,
                                                  author_last_name)
    if abstracts_by_author == 'There are no abstracts from this author.':
        return FAILURE_DEFAULT
    total_abstracts = len(abstracts_by_author)

    abstracts_with_competency = get_abstracts_with_competency(conn,
                                                              competency_id,
                                                              author_id)
    if abstracts_with_competency == []:
        return FAILURE_DEFAULT
    amount_abstracts_with_competency = len(abstracts_with_competency)

    proportion_competency = amount_abstracts_with_competency / total_abstracts
    mean_relevancy = np.mean(relevancies)

    # no bonus if 1/1 abstract shows competency
    if amount_abstracts_with_competency != 1 and total_abstracts != 1:
        bonus = proportion_competency * (1 - mean_relevancy)
    else:
        bonus = 0

    # calculation of relevancy: relevancy mean plus bonus for proportion with the competency
    ranking_score = mean_relevancy + bonus

    return ranking_score


def get_author_name(conn, author_id: int) -> list[str, str]:
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


def get_all_authors(conn) -> list[int, str, str]:
    """Returns all entries in the author relation in the database.

    Args:
        conn (Connection): Connection to the database

    Returns:
        list: list[author_id, first_name, last_name]
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


def change_status(conn, author_id: int, competency_id: int,
                  competency_status: str) -> list[str]:
    """Changes given competency status in database of author with competency

    Args:
        conn (Connection): Connection to the database
        author_id: author where it should be changed
        competency_id: for which competency the status should be changed
        
    
    """
    sql_change_status = """ UPDATE has_competency
                            SET status = ?
                            WHERE author_id = ? AND
                            competency_id = ?
                        """
    cursor = conn.cursor()
    cursor.execute(sql_change_status,
                   (competency_status, author_id, competency_id))
    cursor.fetchall()
    conn.commit()
    result = ["success"]
    return result


def get_author_id_by_full_name(conn, full_name: str) -> int:
    """Returns the id of an author by its name or creates an id if the author's
    id has not been created yet.

    Args:
        conn (Connection): Connection to the database
        full_name (str): Full name of the author

    Returns:
        int: Id of the author
    """
    sql_get_author_id_by_full_name = """SELECT author_id
                           FROM author
                           WHERE first_name || ' ' || last_name = 
                           '{}'""".format(full_name)
    cursor = conn.cursor()
    cursor.execute(sql_get_author_id_by_full_name)
    result = cursor.fetchone()
    conn.commit()
    return result
