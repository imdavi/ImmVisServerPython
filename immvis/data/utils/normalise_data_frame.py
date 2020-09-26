from pandas import DataFrame
import typing
from sklearn.preprocessing import MinMaxScaler
import numpy as np

def normalise_data_frame(data_frame: DataFrame) -> DataFrame:
    result = data_frame.copy()

    for column_name in result.columns:
        column = result[column_name]

        if not np.issubdtype(column.dtype, np.number):
            result[column_name] = column.factorize()[0]

    result[result.columns] = MinMaxScaler().fit_transform(result[result.columns])

    return result

