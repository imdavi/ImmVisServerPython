from pandas import DataFrame
import numpy as np
from ..proto.immvis_pb2 import DatasetToPlot, DatasetRow


def map_dataset_to_plot(data_frame: DataFrame) -> DatasetToPlot:
    normalized_data_frame = _normalize_values(data_frame)

    return DatasetRow(
        rows=map(lambda row: DatasetRow(rowValues=row),
                 normalized_data_frame.values)
    )


def _normalize_values(data_frame: DataFrame) -> DataFrame:
    result = data_frame.copy()

    for column_name in result.columns:
        column = result[column_name]

        if not np.issubdtype(column.dtype, np.number):
            column = column.factorize()[0]

        max_value = column.max()

        min_value = column.min()

        result[column_name] = (column - min_value) / \
            (max_value - min_value)

    return result
