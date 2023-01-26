""" This module fills the database created with create_db
    with data from a csv file and ML generated
    data from the model_api.
"""

import os
import pandas as pd
from langdetect import detect
from db_creation import string_formatter
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

DEFAULT_STATUS = "Unvalidated"


def get_df_from_csv(PATH_TO_FILE):
    """Returns a dataframe from a csv file.

    Args:
        PATH_TO_FILE (str): Path to the csv file.

    Returns:
        DataFrame: DataFrame from the csv file.
    """
    return pd.read_csv(PATH_TO_FILE)


def fill_database_from_added_entries():
    """Fills database with all entries which haven't
    been added to the database yet.
    Safes all entries in current.csv.
    """
    new_entries = get_new_entries()
    fill_database(new_entries)
    # Safe all Entries to current.csv
    all_entries = get_all_entries()
    all_entries.to_csv("db_creation/csv_files/current.csv", index=False)


def get_all_entries() -> pd.DataFrame:
    """Returns all entries, meaning those in the database already and those,
    which are waiting to be added.

    Returns:
        pd.DataFrame: DataFrame with all entries
    """
    df_added_entries = pd.read_csv("db_creation/csv_files/last_added.csv")
    df_current_entries = pd.read_csv("db_creation/csv_files/current.csv")
    return pd.concat([df_added_entries, df_current_entries], ignore_index=True, verify_integrity=True)


def get_new_entries() -> pd.DataFrame:
    """Returns all last added entries, which haven't been in the database yet

    Returns:
        pd.DataFrame: Dataframe of all entirely new entries
    """
    df_added_entries = pd.read_csv("db_creation/csv_files/last_added.csv")
    df_current_entries = pd.read_csv("db_creation/csv_files/current.csv")
    return find_difference(df_added_entries, df_current_entries)


def find_difference(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    """Returns datframe with all entries in df1 which are not in df2.

    Args:
        df1 (dataframe): first dataframe
        df2 (dataframe): second dataframe

    Returns:
        dataframe: difference between dataframes
    """
    return df1[~df1.isin(df2)].dropna()


def build():
    """Builds the database from the csv file.
    """
    fill_database(get_df_from_csv(PATH_TO_FILE))


def fill_database(df):
    """Fills the database with the data from a given dataframe.

    Args:
        df (DataFrame): DataFrame with data for the database.
    """
    # Filters out rows with nan values
    df = df[~df.isnull().any(axis=1)]

    conn = adapter.create_connection()

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
        abstract_id = adapter.get_first_available_abstract_id(conn)

        competencies = get_request_from_api(
            "/get_competency/" + abstract_content)
        print(competencies)
        competency_ids = {}
        for competency in competencies:
            competency_name = competency[0]
            relevancy = competency[1]

            # get or create new id for competency
            competency_ids[competency_name] = adapter.get_or_generate_competency_id_by_name(
                conn, competency_name)
            print(competency_ids[competency_name])
            # get category of competency from model_api
            category_id = get_request_from_api(
                "/get_category_of_competency/" + competency_name)

            adapter.insert_derived_from(conn, competency_ids[competency_name],
                                        abstract_id=abstract_id,
                                        relevancy=relevancy)
            adapter.insert_has_category(conn, category_id,
                                        competency_ids[competency_name])

        for author in authors:
            first_name, last_name = string_formatter.get_first_and_last_name(
                author)
            author_id = adapter.get_author_id_by_name(conn,
                                                      first_name=first_name,
                                                      last_name=last_name)
            adapter.insert_written_by(conn,
                                      abstract_id=abstract_id,
                                      author_id=author_id)
            for competency in competencies:
                competency_name = competency[0]
                adapter.insert_has_competency(conn, author_id=author_id,
                                              competency_id=competency_ids[
                                                competency_name],
                                              status=DEFAULT_STATUS)

        adapter.insert_abstract(conn,
                                (abstract_id, year, abstract_title,
                                    abstract_content, doctype, institution))
