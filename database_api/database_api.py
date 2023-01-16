"""
This is the backend's database_api. It contains the endpoints
to access the database.
"""

from fastapi import FastAPI
import adapter

app = FastAPI()


@app.get("/")
async def root():
    """This is the root endpoint of the database_api. It returns
    a welcome message for the database_api.

    Returns:
        str: String containing a welcome message for the database_api.
    """
    return ("This is the database_api. It contains the endpoints to access "
            "the database. For more details, please "
            "visit http://localhost:8020/docs")


@app.get("/all_categories")
async def get_categories():
    """Endpoint to get all categories of competencies from the database.

    Returns:
        list: List[category_id, name]
    """
    conn = adapter.create_connection()
    response = adapter.get_all_categories(conn)
    conn.close()
    return response

@app.get("/all_competencies/")
async def get_all_competencies():
    conn = adapter.create_connection()
    response = adapter.get_all_competencies(conn)
    conn.close()
    return response


@app.get("/competencies_by_category_id/{category_id}")
async def get_competencies(category_id):
    """Endpoint to get all competencies of a
    certain category from the database.

    Args:
        category_id (int): The id of the category.

    Returns:
        list: List[competency_id, competency_name]
    """
    conn = adapter.create_connection()
    response = adapter.get_competencies_by_category_id(conn, category_id)
    conn.close()
    return response


@app.get("/competencies_by_author_id/{author_id}")
async def get_competencies_by_author(author_id):
    """Endpoint to get all competencies of a
    specific author from the database.

    Args:
        author_id (int): The id of the author.

    Returns:
        list: List[competency_id, competency_name, status]
    """
    conn = adapter.create_connection()
    response = adapter.get_competencies_by_author_id(conn, author_id)
    conn.close()
    return response


@app.get("/competencies_by_abstract_id/{abstract_id}")
async def get_competencies_by_abstract(abstract_id):
    """Endpoint to get all that have been extracted from a specific abstract.

    Args:
        abstract_id (int): The id of the abstract.

    Returns:
        list: List[competency_id, competency_name, relevancy]
    """
    conn = adapter.create_connection()
    response = adapter.get_competencies_by_abstract_id(conn, abstract_id)
    conn.close()
    return response


@app.get("/authors_by_competency_id/{competency_id}")
async def authors_by_competency_id(competency_id):
    """Endpoint to get all authors that have a specific competency.

    Args:
        competency_id (int): The id of the competency.

    Returns:
        list: List[author_id, first_name, last_name, relevancy, status]
    """
    conn = adapter.create_connection()
    response = adapter.get_authors_by_competency_id(conn, competency_id)
    conn.close()
    return response


@app.get("/author_by_abstract_id/{abstract_id}")
async def get_author_by_abstract(abstract_id):
    """Endpoint to get the authors of a specific abstract.

    Args:
        abstract_id (int): The id of the abstract.

    Returns:
        list: List[author_id, first_name, last_name]
    """
    conn = adapter.create_connection()
    response = adapter.get_authors_by_abstract(conn, abstract_id)
    conn.close()
    return response


@app.get("/abstract_by_id/{abstract_id}")
async def get_abstract_by_id(abstract_id):
    """Endpoint to get an abstract by its id.

    Args:
        abstract_id (int): The id of the abstract.

    Returns:
        list: List[abstract_id, year, title, content, doctype, institution]
    """
    conn = adapter.create_connection()
    response = adapter.get_abstract_by_id(conn, abstract_id)
    conn.close()
    return response


@app.get("/abstract_by_author/{first_name}/{last_name}")
async def get_abstract_by_author(first_name, last_name):
    """Endpoint to get all abstracts of a specific author.

    Args:
        first_name (str): The first name of the author.
        last_name (str): The last name of the author.

    Returns:
        list: List[abstract_id, year, title, content, institution]
    """
    conn = adapter.create_connection()
    response = adapter.get_abstracts_by_author(conn, first_name, last_name)
    conn.close()
    return response


# @app.get("/relevancy/{author_id}/{competency_id}")
# async def getrelevancy(author_id, competency_id):
#     """Endpoint to get the relevancy of a competency for an author.

#     Args:
#         author_id (int): The id of the author.
#         competency_id (int): The id of the competency.

#     Returns:
#         int: The relevancy of the competency for the author.
#     """
#     conn = adapter.create_connection()
#     response = adapter.get_relevancy(conn, author_id, competency_id)
#     conn.close()
#     return response


@app.get("/category_name/{category_id}")
async def getcategoryname(category_id):
    """Endpoint to get the name of a category by its id.

    Args:
        category_id (int): The id of the category.

    Returns:
        str: The name of the category.
    """
    conn = adapter.create_connection()
    response = adapter.get_category_name_by_id(conn, category_id)
    conn.close()
    return response


@app.get("/competency_name_by_id/{competency_id}")
async def get_competency_name_by_id(competency_id):
    """Endpoint to get the name of a competency by its id.

    Args:
        competency_id (int): The id of the competency.

    Returns:
        str: The name of the competency.
    """
    conn = adapter.create_connection()
    response = adapter.get_competency_name_by_id(conn, competency_id)
    conn.close()
    return response


@app.get("/competency_id_by_name/{competency_name}")
async def get_competency_id_by_name(competency_name):
    """Endpoint to get the id of a competency by its name.

    Args:
        competency_name (str): The name of the competency.

    Returns:
        int: The id of the competency.
    """
    conn = adapter.create_connection()
    response = adapter.get_competency_id_by_name(conn, competency_name)
    conn.close()
    return response


@app.get("/all_authors")
async def get_authors():
    """Endpoint to get all authors from the database.

    Returns:
        list: List[author_id, first_name, last_name]
    """
    conn = adapter.create_connection()
    response = adapter.get_all_authors(conn)
    conn.close()
    return response
