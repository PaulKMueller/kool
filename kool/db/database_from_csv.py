import pandas as pd
import sqlite3
from sqlite3 import Error
import re

PATH_TO_FILE = "data.csv"
# Path to existing database or where the database should be created
PATH_TO_DB = r"database.db"

def create_connection():
    """ create connection to database or create db if not existent"""
    conn = None
    try:
        conn = sqlite3.connect(PATH_TO_DB)
    except Error as e:
        print(e)
    
    return conn

def insert_abstract(conn, db_entry_abstract):
    '''Inserts abstract in database'''
    sql_command = """INSERT INTO abstracts(abstract_id, year, abstract_title, abstract_content, doctype, institution)
                    VALUES(?,?,?,?,?,?)"""
    c = conn.cursor()
    c.execute(sql_command, db_entry_abstract)
    conn.commit()

def insert_written_by(conn, db_entry_abstract):
    '''inserts written_by in database'''
    sql_command = """INSERT INTO written_by(abstract_id, author_name)
                    VALUES(?,?)"""
    c = conn.cursor()
    c.execute(sql_command, db_entry_abstract)
    conn.commit()

def format_authors(raw_authors):
    '''Formatting authors. WARNING: This method depends on the "style" authors are described in KIT Open'''
    authors_splitted = raw_authors.split(";")
    authors_formatted = []
    for author in authors_splitted:
        author_without_footnote = re.split("[0-9]", author)[0]  # There are footnotes represented as numbers 
        if not "... mehr" in author:                            # unfortunately "... mehr" was hardcoded as author text
            authors_formatted.append(author_without_footnote.replace(" ", ""))
        else:
            continue
    return authors_formatted

conn = create_connection()

df  = pd.read_csv(PATH_TO_FILE)
df = df[~df.isnull().any(axis=1)] # Filters out rows with nan values 

for index, row in df.iterrows():
    '''This loop iterates the rows and stores calls the inserting functions'''

    abstract_title = row.loc["Title"]
    doctype = row.loc["Doc-Type"]
    authors = format_authors(row.loc["Authors"])
    year = row.loc["Year"]
    institution = row.loc["Institutions"]
    abstract_content = row.loc["Abstract"]

    for author in authors:
        insert_written_by(conn, (index, author))

    insert_abstract(conn, (index, year, abstract_title, abstract_content, doctype, institution))