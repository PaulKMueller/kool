"""Contains functionality refering the database_info.json"""
import json

PATH_TO_DB_INFO = "databases/database_info.json"


def get_active_db_name() -> str:
    """returns db name of the database which is active. Returns
    empty str if no db is active

    Returns:
        str: db name of active db
    """
    dict = load_dict()
    for key, value in dict.items():
        if value['active'] == 'True':
            return key
    return ''


def change_db_active_status(database_name: str, new_status: str):
    """changes the active status (meaning whether the db is the one
    used in frontend).

    Args:
        database_name (str): db_name of database which active status should be 
                             changed
        new_status (str): new status ("True" or "False")
    """
    dict = load_dict()
    dict[database_name]['active'] = new_status
    write_dict_to_json(dict=dict)


def get_db_name_from_path_to_db(path_to_db: str) -> str:
    """Returns name of database to a given path, given its info is
    stored in database_info.

    Args:
        path_to_db (str): path to db which name is of interest

    Returns:
        str: name of database with specified path
    """    
    dict = load_dict()
    for db_name, db_data in dict.items():
        if db_data["path"] == path_to_db:
            return db_name
    return ""


def get_db_path_from_db_name(db_name: str) -> str:
    """Returns path of database to a given db name, given its info is
    stored in database_info.

    Args:
        db_name (str): name of the database which path is of interest

    Returns:
        str: path to database with specified name
    """
    dict = load_dict()
    return dict[db_name]["path"]


def safe_new_database_info(db_name: str, path_to_db: str, model: str,
                           generated: str, is_running: str):
    """Add new database to the database info json. 

    Args:
        db_name (str): Name of new database
        path_to_db (str): path to new database from main dir (database_api)
        model (str): Model which generated the competencies
        generated (str): timestamp when the database creation started
        is_running (str): string with "True" or "False" whether db is building
    """
    dict = load_dict()
    dict[db_name] = {"model": model,
                     "generated": generated,
                     "path": path_to_db,
                     "active": "False",
                     "build_status": {
                        "is_running": is_running,
                        "at": 0,
                        "from": 0}}
    write_dict_to_json(dict=dict)


def increase_abstract_count(db_name: str, add_count: int):
    """Increase total abstract count.

    Args:
        db_name (str): name of database which should be edited
        add_count (int): int how much abstract count should be increased
    """
    dict = load_dict()
    current_count = dict[db_name]["build_status"]["from"]
    dict[db_name]["build_status"]["from"] = current_count + add_count
    write_dict_to_json(dict=dict)


def increase_build_status(db_name: str, add_count: int):
    """Increases build status .

    Args:
        db_name (str): name of database which should be edited
        add_count (int): int how much build status should be increased
    """
    dict = load_dict()
    current_count = dict[db_name]["build_status"]["at"]
    dict[db_name]["build_status"]["at"] = current_count + add_count
    write_dict_to_json(dict=dict)


def update_build_status_stopped(db_name: str):
    """Updates build status to stopped

    Args:
        db_name (str): name of database which should be edited
    """
    dict = load_dict()
    dict[db_name]["build_status"]["is_running"] = "False"
    write_dict_to_json(dict=dict)


def load_dict() -> dict:
    """Loads database info json file as a dictionary

    Returns:
        dict: dictionary of database info json
    """
    with open(PATH_TO_DB_INFO, "r") as f:
        dict = json.load(f)
    return dict


def get_database_info() -> str:
    """Returns database info json as string

    Returns:
        str: String of database info json
    """
    with open(PATH_TO_DB_INFO, "r") as f:
        return f.read()


def write_dict_to_json(dict: dict):
    """Writes given dictionary to database info json. Overwrites
    file. Use :func:`safe_new_database_info()` when adding a database

    Args:
        dict (dict): dictionary which will be written in json file
    """
    with open(PATH_TO_DB_INFO, "w") as f:
        json.dump(dict, f)
