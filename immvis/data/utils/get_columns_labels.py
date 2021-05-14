from pandas import DataFrame
import typing
from sklearn.preprocessing import MinMaxScaler
import numpy as np

_AXIS_DIVISIONS = 10

def get_columns_labels(data_frame: DataFrame, columns: typing.List[str]) -> typing.List[typing.List[str]]:
    result: typing.List[typing.List[str]] = []

    for index, _ in enumerate(data_frame.columns):
        column = data_frame.iloc[:,index]

        column_labels: typing.List[str] = []

        if not np.issubdtype(column.dtype, np.number):
            column_labels = list(map(lambda label: str(label), column.unique()))
        else:
            min_value = column.min()
            max_value = column.max()
            column_labels = list(map(lambda number: str(round(number, 2)), np.linspace(min_value, max_value, _AXIS_DIVISIONS)))

        result.append(column_labels)

    return result
