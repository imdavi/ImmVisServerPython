from .extutils import is_csv, is_excel, is_json, is_image
from .imgdataset import read_image_as_dataframe
import pandas as pd
from .exceptions import UnknownDatasetType

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

def get_data_frame_rows_as_list(data_frame):
    for _, row in enumerate(data_frame.values):
        row_values_list = row.tolist()
        yield row_values_list
