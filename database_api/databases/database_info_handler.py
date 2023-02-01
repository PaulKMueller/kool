import json

PATH_TO_DB_INFO = "databases/database_info.json"


def get_active_db_name() -> str:
    dict = load_dict()
    for key, value in dict.items():
        if value['active'] == 'True':
            return key

    return ''


def change_db_active_status(database_name: str, new_status: str):
    dict = load_dict()
    dict[database_name]['active'] = new_status
    write_dict_to_json(dict=dict)


def safe_new_database_info(db_name: str, path_to_db: str, model: str, generated: str):
    dict = load_dict()
    dict[db_name] = {"model": model,
                     "generated": generated,
                     "path": path_to_db,
                     "active": "False",
                     # TODO: change to real status
                     "status": {
                        "is_running": "False",
                        "at": 3500,
                        "from": 3500}}
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