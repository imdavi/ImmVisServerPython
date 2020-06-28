from .datasets_folder import get_datasets_folder_path
from .extension_utils import is_csv, is_excel, is_json
import typing
from os import listdir
from os.path import isdir

def list_available_datasets() -> typing.List[str]:
    datasets_folder_path = get_datasets_folder_path()

    available_datasets = []

    if isdir(datasets_folder_path):
        files_names = listdir(datasets_folder_path)

        for file_name in files_names:
            if is_csv(file_name) or is_excel(file_name) or is_json(file_name):
                available_datasets.append(file_name)

    return available_datasets
    