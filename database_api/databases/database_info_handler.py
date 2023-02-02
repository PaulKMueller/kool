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


def get_db_name_from_path_to_db(path_to_db: str):
    """Returns name of database to a given path, given its info is
    stored in database_info.

    Args:
        path_to_db (str): path to db which name is of interest

    Returns:
        _type_: _description_
    """    
    dict = load_dict()
    for db_name, db_data in dict.items():
        if db_data["path"] == path_to_db:
            return db_name
    return ""


def get_db_path_from_db_name(db_name: str):
    dict = load_dict()
    return dict[db_name]["path"]


def safe_new_database_info(db_name: str, path_to_db: str, model: str, generated: str,
                           is_running: str):
    dict = load_dict()
    dict[db_name] = {"model": model,
                     "generated": generated,
                     "path": path_to_db,
                     "active": "False",
                     # TODO: change to real status
                     "build_status": {
                        "is_running": is_running,
                        "at": 0,
                        "from": 0}}
    write_dict_to_json(dict=dict)


def add_to_abstract_count(db_name: str, add_count: int):
    dict = load_dict()
    current_count = dict[db_name]["build_status"]["from"]
    dict[db_name]["build_status"]["from"] = current_count + add_count
    write_dict_to_json(dict=dict)


def add_to_build_status(db_name: str, add_count: int):
    dict = load_dict()
    current_count = dict[db_name]["build_status"]["at"]
    dict[db_name]["build_status"]["at"] = current_count + add_count
    write_dict_to_json(dict=dict)


def update_build_status_stopped(db_name: str):
    dict = load_dict()
    dict[db_name]["build_status"]["is_running"] = "False"
    write_dict_to_json(dict=dict)


def load_dict() -> dict:
    with open(PATH_TO_DB_INFO, "r") as f:
        dict = json.load(f)
    return dict


def get_database_info() -> str:
    with open(PATH_TO_DB_INFO, "r") as f:
        return f.read()


def write_dict_to_json(dict: dict):
    with open(PATH_TO_DB_INFO, "w") as f:
        json.dump(dict, f)