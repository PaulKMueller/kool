""" This file creates a database from a csv file.
"""

import pandas as pd
from langdetect import detect
import string_formatter
import yaml
import adapter
from tqdm import tqdm
import models

with open("kool-backend/database_api/db_creation/db_config.yml", "r",
          encoding='utf-8') as ymlfile:
    cfg = yaml.safe_load(ymlfile)

# Path to existing csv file with data for the database
PATH_TO_FILE = cfg["paths"]["path_to_csv"]

# Path to existing database or where the database should be created
PATH_TO_DB = cfg["paths"]["path_to_db"]

df = pd.read_csv(PATH_TO_FILE)

# Filters out rows with nan values
df = df[~df.isnull().any(axis=1)]

conn = adapter.create_connection()

# Inserts categories for competencies
for index, category in enumerate(cfg["categories"]):
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

    competencies = models.get_competency_from_backend(abstract_content)
    competency_ids = {}

    for competency in competencies:
        competency_name = competency[0]
        relevancy = competency[1]
        competency_ids[competency] = adapter.get_competency_id_by_name(
            conn, competency_name)
        category_id = int(models.get_category_of_competence(
            competency_ids[competency]))
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
