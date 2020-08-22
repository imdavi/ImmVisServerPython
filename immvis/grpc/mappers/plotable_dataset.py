from pandas import DataFrame, Series
import numpy as np
from ..proto.immvis_pb2 import DatasetToPlot, DatasetRow
from sklearn.preprocessing import MinMaxScaler


def map_dataset_to_plot(data_frame: DataFrame) -> DatasetToPlot:
    normalized_data_frame = _normalize_values(data_frame)

    return DatasetToPlot(
        rows=list(map(lambda row: DatasetRow(rowValues=row),
                 normalized_data_frame.values))
    )


def _normalize_values(data_frame: DataFrame) -> DataFrame:
    result = data_frame.copy()

    for column_name in result.columns:
        column = result[column_name]

        if not np.issubdtype(column.dtype, np.number):
            result[column_name] = column.factorize()[0]

    result[result.columns] = MinMaxScaler().fit_transform(result[result.columns])

    return result
