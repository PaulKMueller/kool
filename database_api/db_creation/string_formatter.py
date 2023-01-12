"""String formatting for database_from_csv.py,
depends on structure of KIT-Open's results"""

import re


def get_first_and_last_name(author_sep_with_comma):
    """Extracts first and last name from a string containing both.

    Args:
        author_sep_with_comma (str): String containing first and last name,
        separated by a comma

    Returns:
        tuple: Tuple(first_name, last_name)
    """

    if "," in author_sep_with_comma:
        # There is sometimes more than one ","
        # in this case only the first two strings are relevant
        splitted = author_sep_with_comma.split(",")
        first_name, last_name = splitted[1].strip(), splitted[0].strip()
    else:
        first_name = ""
        last_name = author_sep_with_comma.strip()
    return first_name, last_name


def format_authors(raw_authors):
    """Formats authors. WARNING: This method depends on the
    format in which authors are described in KIT Open.

    Args:
        raw_authors (list): List of authors as strings in original format

    Returns:
        list: List of authors as strings in formatted format
    """

    authors_splitted = raw_authors.split(";")
    authors_formatted = []
    for author in authors_splitted:

        # There are footnotes represented as numbers
        author_without_footnote = re.split("[0-9]", author)[0]

        # unfortunately "... mehr" was hardcoded as author text
        if "... mehr" not in author:
            authors_formatted.append(author_without_footnote)
        else:
            continue
    return authors_formatted
