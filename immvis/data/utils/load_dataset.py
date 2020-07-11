from .datasets_folder import get_datasets_folder_path
from .extension_utils import is_csv, is_excel, is_json
from os.path import join, isfile
from pandas import DataFrame, read_csv, read_excel, read_json


class UnknownDatasetType(Exception):
    pass


def load_data_frame(dataset_path: str) -> DataFrame:
    datasets_folder_path = get_datasets_folder_path()

    path_on_datasets_folder = join(datasets_folder_path, dataset_path)

    path_to_open = path_on_datasets_folder

    if not isfile(path_on_datasets_folder):
        path_to_open = dataset_path

    return _open_dataset_file(path_to_open)


def _open_dataset_file(file_path: str) -> DataFrame:
    data_frame = None

    if is_csv(file_path):
        data_frame = read_csv(file_path)
    elif is_json(file_path):
        data_frame = read_json(file_path)
    elif is_excel(file_path):
        data_frame = read_excel(file_path)
    else:
        raise UnknownDatasetType

    return data_frame
