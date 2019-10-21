import json
from typing import Callable
from typing import Dict
from typing import List
import os


def update(file_path: str, transformation: Callable[[List], None], out_file_path: str = None, **kwargs) -> None:
    __do_update_json(file_path, out_file_path, transformation, **kwargs)


def update(file_path: str, transformation: Callable[[Dict], None], out_file_path: str = None, **kwargs) -> None:
    __do_update_json(file_path, out_file_path, transformation, **kwargs)


def __do_update_json(in_file_path, out_file_path, transformation, **kwargs):
    if out_file_path is None:
        out_file_path = in_file_path

    data = read_original_json(in_file_path)

    transformation(data)
    json.dumps(data)  # crash here if sth goes wrong

    save_modified_json(data, kwargs, out_file_path)


def read_original_json(in_file_path):
    with open(in_file_path, "r") as inFile:
        data = json.load(inFile)
    return data


def set_param_value_if_not_set(kwargs, key, value=None):
    if key not in kwargs:
        kwargs[key] = value


def save_modified_json(data, kwargs, out_file_path):
    set_param_value_if_not_set(kwargs, "indent", 4)
    set_param_value_if_not_set(kwargs, "sort_keys", True)

    dir_name = os.path.dirname(out_file_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    with open(out_file_path, "w") as outFile:
        json.dump(data, outFile, **kwargs)
