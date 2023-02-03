""" This module fills the database created with create_db
    with data from a csv file and ML generated
    data from the model_api.
"""
import os
import pandas as pd

from langdetect import 
import requests

from db_creation.model_endpoint import ENDPOINT
from db_creation import string_formatter
from databases import database_info_handler
import adapter

ENVIRONMENT_VARIABLE_MODEL_API_PORT = "MODEL_API_PORT"
MODEL_API_PORT = os.environ.get(ENVIRONMENT_VARIABLE_MODEL_API_PORT)

URL_OF_MODEL_API = "http://model_api:" + MODEL_API_PORT

# Path to existing csv file with data for the database
ENVIRONMENT_VARIABLE_CSV_FILE = "PATH_TO_CSV"
PATH_TO_FILE = os.environ.get(ENVIRONMENT_VARIABLE_CSV_FILE)

PATH_TO_CURRENT_CSV = PATH_TO_FILE
PATH_TO_LAST_ADDED_CSV = "db_creation/csv_files/last_added.csv"

# Path to existing database or where the database should be created
ENVIRONMENT_VARIABLE_DB_FILE = "PATH_TO_DB"
PATH_TO_DB = os.environ.get(ENVIRONMENT_VARIABLE_DB_FILE)

# Default status of a competency added to the db
DEFAULT_STATUS = "Unvalidated"

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


def get_df_from_csv(path_to_file: str) -> pd.DataFrame:
    """Returns a dataframe from a csv file.

    Args:
        path_to_file (str): Path to the csv file.

    Returns:
        DataFrame: DataFrame from the csv file.
    """
    return pd.read_csv(path_to_file)


def fill_database_from_added_entries(model: str):
    """Fills database with all entries which haven't
    been added to the database yet.
    Safes all entries in current.csv.

    Args:
        model (str): Model which should be used to get the
        competencies, consult model_endpoint.py for accepted models
    """
    new_entries = get_new_entries()
    active_db_name = database_info_handler.get_active_db_name()
    # using active_db_path to append currently active database
    active_db_path = database_info_handler.get_db_path_from_db_name(active_db_name)
    fill_database(df=new_entries, model=model, path_to_db=active_db_path)
    # Safe all Entries to current.csv
    all_entries = get_all_entries()
    all_entries.to_csv(PATH_TO_CURRENT_CSV, index=False)


def build(model: str, path_to_db: str):
    """Builds the database from the current.csv file.

    Args:
        model (str): Model which should be used to get the
        competencies, consult model_endpoint.py for accepted models
        path_to_db (str): Path to the database which should be filled
    """
    fill_database(df=get_df_from_csv(PATH_TO_FILE), model=model, path_to_db=path_to_db)


def get_all_entries() -> pd.DataFrame:
    """Returns all entries, meaning those in the database already and those,
    which are waiting to be added.

    Returns:
        pd.DataFrame: DataFrame with all entries
    """
    df_added_entries = pd.read_csv(PATH_TO_LAST_ADDED_CSV)
    df_current_entries = pd.read_csv(PATH_TO_CURRENT_CSV)
    return pd.concat([df_added_entries, df_current_entries],
                     ignore_index=True,
                     verify_integrity=True)


def get_new_entries() -> pd.DataFrame:
    """Returns all last added entries, which haven't been in the database yet

    Returns:
        pd.DataFrame: Dataframe of all entirely new entries
    """
    df_added_entries = pd.read_csv(PATH_TO_LAST_ADDED_CSV)
    df_current_entries = pd.read_csv(PATH_TO_CURRENT_CSV)
    return find_difference(df_added_entries, df_current_entries)


def find_difference(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    """Returns datframe with all entries in df1 which are not in df2.

    Args:
        df1 (dataframe): first dataframe
        df2 (dataframe): second dataframe

    Returns:
        dataframe: difference between dataframes
    """
    # perform leftjoin 
    df_merged = df1.merge(df2.drop_duplicates(),
                          how="left",
                          on="Abstract",
                          indicator=True,
                          suffixes=("", "_y"))
    difference = df_merged.query("_merge == 'left_only'")[df1.columns]
    return difference


def filter_rows_with_nan_values(df: pd.DataFrame) -> pd.DataFrame:
    """Filters out rows with nan values

    Args:
        df (pd.DataFrame): Dataframe to be filtered

    Returns:
        pd.DataFrame: filtered Dataframe
    """
    return df[~df.isnull().any(axis=1)]


def get_entries_from_row(row: pd.Series):
    """Returns the values of a row of a dataframe which results
    from reading the csv.

    Args:
        row (pd.Series): row of the specific dataframe resulting
        from reading the csv. Must have Columns Abstract, Title,
        Doc-Type, Authors, Year and Institutions 

    Returns:
        tuple: tuple of the Values mentioned above
    """    
    abstract_content = string_formatter.format_for_api_request(row.loc["Abstract"])
    abstract_title = row.loc["Title"]
    doctype = row.loc["Doc-Type"]
    authors = string_formatter.format_authors(row.loc["Authors"])
    year = row.loc["Year"]
    institution = row.loc["Institutions"]

    return abstract_content, abstract_title, doctype, authors, year, institution


def is_english(text: str) -> bool:
    """Checks if a text is english using langdetect

    Args:
        text (str): the text to check for language

    Returns:
        bool: True if text is english
    """
    return detect(text) == "en"


def add_competency_to_db(conn, competency: list, competency_ids: dict,
                         abstract_id: int):
    """Adds competency to db including generating a new competency when
    competency not in db yet and matching the competency to it's corresponding
    abstract and category (and adding this info in the db too)

    Args:
        conn (Connection): Connection to the database
        competency (list): List of to containing the competency itself and its
                           relevancy (=/= ranking; generated by model)
        competency_ids (dict): dict storing each id too its competency
        abstract_id (int): id of the abstract containing the competency
    """    
    competency_name = competency[0]
    relevancy = competency[1]

    # get or create new id for competency
    competency_ids[competency_name] = adapter.get_or_generate_competency_id_by_name(
        conn, competency_name)
    # get category of competency from model_api
    category_id = get_request_from_api(
        "/get_category_of_competency/" + string_formatter.format_for_api_request(competency_name))
    adapter.insert_derived_from(conn, competency_ids[competency_name],
                                abstract_id=abstract_id,
                                relevancy=relevancy)
    adapter.insert_has_category(conn, category_id,
                                competency_ids[competency_name])


def add_author_to_db(conn, author: str, abstract_id: int, competency_ids: dict):
    """Adds author to db including matching the author to its competencies
    and written abstract.

    Args:
        conn (Connection): Connection to the database
        author (str): author as string (in the representation retrieved from
                      KIT Open)
        abstract_id (int): id of the abstract
        competency_ids (dict): dict storing each id too its competency
    """
    first_name, last_name = string_formatter.get_first_and_last_name(
                    author)
    author_id = adapter.get_author_id_by_name(conn,
                                              first_name=first_name,
                                              last_name=last_name)
    adapter.insert_written_by(conn,
                              abstract_id=abstract_id,
                              author_id=author_id)

    for competency_name, competency_id in competency_ids.items():
        adapter.insert_has_competency(conn, author_id=author_id,
                                      competency_id=competency_id,
                                      status=DEFAULT_STATUS)   


def fill_database(df, model: str, path_to_db: str):
    """Fills the database with the data from a given dataframe.

    Args:
        df (DataFrame): DataFrame with data for the database.
        path_to_db (str): Path to Database which should be filled 
    """
    df = filter_rows_with_nan_values(df=df)
    COMPETENCY_ENDPOINT = ENDPOINT.get_endpoint(model)

    conn = adapter.create_connection_to(path_to_db=path_to_db)

    total_number_of_abstracts = df.shape[0]

    db_name = database_info_handler.get_db_name_from_path_to_db(path_to_db=path_to_db)
    database_info_handler.increase_abstract_count(db_name=db_name,
                                                  add_count=total_number_of_abstracts)
    try:
        # This loop iterates the rows and stores calls the inserting functions
        for index, row in df.iterrows():
            database_info_handler.increase_build_status(db_name=db_name,
                                                        add_count=1)

            abstract_content, abstract_title, doctype, authors, year, institution = get_entries_from_row(row=row)
            # We focus on english abstracts
            if not is_english(abstract_content):
                continue

            abstract_id = adapter.get_first_available_abstract_id(conn)
            competencies = get_request_from_api(
                COMPETENCY_ENDPOINT + abstract_content)
            
            competency_ids = {}
            for competency in competencies:
                add_competency_to_db(conn=conn, competency=competency,
                                     competency_ids=competency_ids,
                                     abstract_id=abstract_id)

            for author in authors:
                add_author_to_db(conn=conn, author=author,
                                 abstract_id=abstract_id,
                                 competency_ids=competency_ids)

            adapter.insert_abstract(conn,
                                    (abstract_id, year, abstract_title,
                                        abstract_content, doctype, institution))
    except Exception as e:
        # Filling db has stopped
        print(e)
        database_info_handler.update_build_status_stopped(db_name=db_name)

    database_info_handler.update_build_status_stopped(db_name=db_name)
