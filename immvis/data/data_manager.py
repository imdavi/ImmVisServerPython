from pandas import DataFrame
import typing
from .utils import list_available_datasets, load_data_frame, get_dataset


class DataManager():
    data_frame: DataFrame = None

    def __init__(self, data_frame: DataFrame = None):
        self.data_frame = data_frame

    def list_available_datasets(self) -> typing.List[str]:
        return list_available_datasets()

    def load_dataset(self, dataset_path: str) -> DataFrame:
        self.data_frame = load_data_frame(dataset_path)
        return self.data_frame

    def get_dataset_to_plot(self, columns_to_plot: typing.List[str]):
        return get_dataset(self.data_frame, columns_to_plot)
