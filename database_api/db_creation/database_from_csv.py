""" This module fills the database created with create_db
    with data from a csv file and ML generated
    data from the model_api.
"""

import os
import pandas as pd
from langdetect import detect
from . import string_formatter
import yaml
import adapter
from tqdm import tqdm
import requests

ENVIRONMENT_VARIABLE_MODEL_API_PORT = "MODEL_API_PORT"
MODEL_API_PORT = os.environ.get(ENVIRONMENT_VARIABLE_MODEL_API_PORT)

URL_OF_MODEL_API = "http://model_api:" + MODEL_API_PORT


def get_request_from_api(endpoint: str):
    """ This function sends a get request to the
    model_api and returns the response as json

    Args:
        endpoint (str): The endpoint of the model_api 

    Returns:
        json: The response of the model_api
    """
    response = requests.get(URL_OF_MODEL_API + endpoint)
    return response.json()


# Path to existing csv file with data for the database
ENVIRONMENT_VARIABLE_CSV_FILE = "PATH_TO_CSV"
PATH_TO_FILE = os.environ.get(ENVIRONMENT_VARIABLE_CSV_FILE)

# Path to existing database or where the database should be created

ENVIRONMENT_VARIABLE_DB_FILE = "PATH_TO_DB"
PATH_TO_DB = os.environ.get(ENVIRONMENT_VARIABLE_DB_FILE)

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



def get_df_from_csv(PATH_TO_FILE):
    return pd.read_csv(PATH_TO_FILE)


def build():
    fill_database(get_df_from_csv(PATH_TO_FILE))


def fill_database(df):
    # Filters out rows with nan values
    df = df[~df.isnull().any(axis=1)]

    conn = adapter.create_connection()

    # Inserts categories for competencies
    for index, category in enumerate(categories):
        adapter.insert_category(conn, category_name=category, category_id=index)

    # This loop iterates the rows and stores calls the inserting functions
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        abstract_content = row.loc["Abstract"]

        # We focus on english abstracts
        if detect(abstract_content) != "en":
            continue

        abstract_title = row.loc["Title"]
        doctype = row.loc["Doc-Type"]
        authors = string_formatter.format_authors(row.loc["Authors"])
        year = row.loc["Year"]
        institution = row.loc["Institutions"]

        competencies = get_request_from_api("/get_competency/" + abstract_content)
        competency_ids = {}

        for competency in competencies:
            competency_name = competency[0]
            relevancy = competency[1]

            # get or create new id for competency
            competency_ids[competency] = adapter.get_competency_id_by_name(
                conn, competency_name)

            # get category of competency from model_api
            category_id = int(get_request_from_api("/get_category_of_competency/" +
                                                competency_name))

            adapter.insert_derived_from(conn, competency_ids[competency],
                                        abstract_id=index, relevancy=relevancy)
            adapter.insert_has_category(conn, category_id,
                                        competency_ids[competency])

        for author in authors:
            first_name, last_name = string_formatter.get_first_and_last_name(
                author)
            author_id = adapter.get_author_id_by_name(conn, first_name, last_name)
            adapter.insert_written_by(conn, index, author_id)
            for competency in competencies:
                competency_name = competency[0]
                adapter.insert_has_competency(conn, author_id,
                                            competency_ids[competency],
                                            "Unvalidated")

        adapter.insert_abstract(conn, (index, year, abstract_title,
                                    abstract_content, doctype, institution))
