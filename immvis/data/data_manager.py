from pandas import DataFrame
import typing
from .utils import list_available_datasets, load_data_frame, normalise_data_frame, generate_data_frame


class DataManager():
    data_frame: DataFrame = None

    def __init__(self, data_frame: DataFrame = None):
        self.data_frame = data_frame

    def list_available_datasets(self) -> typing.List[str]:
        return list_available_datasets()

    def load_dataset(self, dataset_path: str) -> DataFrame:
        self.data_frame = load_data_frame(dataset_path)
        return self.data_frame

    def get_normalised_dataset(self, columns: typing.List[str]):
        data_frame_to_normalise: DataFrame = None

        if len(columns) > 0:
            data_frame_to_normalise = self.data_frame[columns]
        else:
            data_frame_to_normalise = self.data_frame

        return normalise_data_frame(data_frame_to_normalise)

    def generate_dataset(self, columns_amount: int, rows_amount: int, centers_amount: int) -> DataFrame:
        self.data_frame = generate_data_frame(columns_amount, rows_amount, centers_amount)
        return self.data_frame
