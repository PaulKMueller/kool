import sqlite3
from sqlite3 import Error

# Path to existing database or where the database should be created
PATH_TO_DB = r"database.db"

# SQL-Commands to create tables
SQL_CREATE_TABLE_ABSTRACTS = """CREATE TABLE IF NOT EXISTS abstracts(
                                    abstract_id int IDENTITY(1,1) PRIMARY KEY,
                                    year int,
                                    abstract_title text NOT NULL,
                                    abstract_content text NOT NULL,
                                    doctype text,
                                    institution text
                                );"""
SQL_CREATE_TABLE_COMPETENCES = """CREATE TABLE IF NOT EXISTS competences(
                                    competence_id varchar(10) PRIMARY KEY,
                                    competence_name text NOT NULL
                                );"""
SQL_CREATE_TABLE_SHOW_COMPETENCE = """CREATE TABLE IF NOT EXISTS shows_competence(
                                    abstract_id int,
                                    competence_id varchar(10),
                                    PRIMARY KEY (abstract_id, competence_id),
                                    FOREIGN KEY (abstract_id) REFERENCES abstracts(abstract_id),
                                    FOREIGN KEY (competence_id) REFERENCES competences(competence_id)
                                );"""
SQL_CREATE_TABLE_WRITTEN_BY = """CREATE TABLE IF NOT EXISTS written_by(
                                    abstract_id int,
                                    author_name text,
                                    PRIMARY KEY (abstract_id, author_name),
                                    FOREIGN KEY (abstract_id) REFERENCES abstracts(abstract_id)
                                );"""       

# All commands                         
sql_commands = [SQL_CREATE_TABLE_ABSTRACTS, SQL_CREATE_TABLE_COMPETENCES, SQL_CREATE_TABLE_SHOW_COMPETENCE, SQL_CREATE_TABLE_WRITTEN_BY]

def create_connection(db_file):
    """ create connection to database or create db if not existent"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    
    return conn

def create_table(conn, sql_command):
    """ create table in db from given command"""
    try:
        c = conn.cursor()
        c.execute(sql_command)
    except Error as e:
        print(e)

conn = create_connection(PATH_TO_DB)

if conn is not None:
    for sql_command in sql_commands:
        create_table(conn, sql_command)
