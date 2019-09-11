from data.utils.extutils import is_csv, is_excel, is_json, is_image
from data.utils.imgdataset import read_image_as_dataframe
import pandas as pd

class UnknownDatasetType(Exception):
    pass

def open_dataset_file(file_path):
    file_path = file_path.strip()

    data_frame = None

    if is_csv(file_path):
        data_frame = pd.read_csv(file_path)
    elif is_json(file_path):
        data_frame = pd.read_json(file_path)
    elif is_excel(file_path):
        data_frame = pd.read_excel(file_path)
    elif is_image(file_path):
        data_frame = read_image_as_dataframe(file_path)
    else:
        raise UnknownDatasetType

    return data_frame
