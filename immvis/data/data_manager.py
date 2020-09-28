from pandas import DataFrame
import typing
from .utils import list_available_datasets, load_data_frame, normalise_data_frame


class DataManager():
    data_frame: DataFrame = None

    def __init__(self, data_frame: DataFrame = None):
        self.data_frame = data_frame

    def _get_data_set_with_selected_columns(self, columns: typing.List[str]) -> DataFrame:
        if columns is not None and len(columns) > 0:
            return self.data_frame[columns]
        else:
            return self.data_frame

    def list_available_datasets(self) -> typing.List[str]:
        return list_available_datasets()

    def load_dataset(self, dataset_path: str) -> DataFrame:
        self.data_frame = load_data_frame(dataset_path)
        return self.data_frame

    def get_normalised_dataset(self, columns: typing.List[str]):
        data_frame_to_normalise: DataFrame = self._get_data_set_with_selected_columns(columns)

        return normalise_data_frame(data_frame_to_normalise)


