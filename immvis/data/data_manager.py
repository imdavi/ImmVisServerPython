from pandas import DataFrame
import typing
from .utils import list_available_datasets, load_data_frame, normalise_data_frame, generate_data_frame, get_columns_labels, do_kmeans_analysis, KMeansAnalysisResult


class DataManager():
    data_frame: DataFrame = None

    def __init__(self, data_frame: DataFrame = None):
        self.data_frame = data_frame

    def list_available_datasets(self) -> typing.List[str]:
        return list_available_datasets()

    def load_dataset(self, dataset_path: str) -> DataFrame:
        self.data_frame = load_data_frame(dataset_path)
        return self.data_frame

    def get_selected_columns(self, columns: typing.List[str]):
        selected_data_frame: DataFrame = None

        if len(columns) > 0:
            selected_data_frame = self.data_frame[columns]
        else:
            selected_data_frame = self.data_frame

        return selected_data_frame

    def get_normalised_dataset(self, columns: typing.List[str]) -> DataFrame:
        return normalise_data_frame(self.get_selected_columns(columns))

    def get_columns_labels(self, columns: typing.List[str]) -> typing.List[typing.List[str]]:
        return get_columns_labels(self.get_selected_columns(columns), columns)

    def generate_dataset(self, columns_amount: int, rows_amount: int, centers_amount: int) -> DataFrame:
        self.data_frame = generate_data_frame(
            columns_amount, rows_amount, centers_amount)
        return self.data_frame

    def do_kmeans_analysis(self, columns: typing.List[str], clusters_number: int) -> KMeansAnalysisResult:
        return do_kmeans_analysis(self.get_selected_columns(columns), clusters_number)
