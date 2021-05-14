from pandas import DataFrame
from sklearn.datasets import make_blobs

_RANDOM_STATE = 435

def generate_data_frame(columns_amount: int, rows_amount: int, centers_amount: int) -> DataFrame:
    samples, labels = make_blobs(n_samples=rows_amount, centers=centers_amount, n_features=columns_amount, random_state=_RANDOM_STATE)

    columns = list(map(lambda number: ('Column ' + str(number+1)),  range(0, columns_amount)))

    return DataFrame(data = samples, columns=columns)
