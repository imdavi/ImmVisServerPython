from os import environ
from os import environ, mkdir, getcwd, listdir
from os.path import join, isdir

_DATASETS_FOLDER_ENV_VARIABLE = 'IMMVIS_DATASETS'
_DEFAULT_DATASETS_FOLDER = join(getcwd(), 'datasets')

def get_datasets_folder_path() -> str:
    datasets_folder_path = environ.get(_DATASETS_FOLDER_ENV_VARIABLE)

    if datasets_folder_path is None or not isdir(datasets_folder_path):
        datasets_folder_path = _DEFAULT_DATASETS_FOLDER

    return datasets_folder_path
