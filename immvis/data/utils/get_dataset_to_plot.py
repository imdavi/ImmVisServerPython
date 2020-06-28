from pandas import DataFrame
import typing

def get_dataset(original_data_frame: DataFrame, columns_to_plot: typing.List[str]=[]) -> DataFrame:
    data_frame = original_data_frame

    if len(columns_to_plot) > 0:
        data_frame = original_data_frame[columns_to_plot]

    return data_frame

