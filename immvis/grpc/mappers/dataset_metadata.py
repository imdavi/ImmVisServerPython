from pandas import DataFrame, Series
from ..proto.immvis_pb2 import DatasetMetadata, Column, ColumnInfo, DescriptiveStatisticsFeature
import typing

def get_dataset_metadata(data_frame: DataFrame) -> DatasetMetadata:
    return DatasetMetadata(
        rowsCount= data_frame.shape[0],
        columnsCount= data_frame.shape[1],
        columnsInfo = map(lambda column_label: _get_column_info(data_frame, column_label), data_frame.columns)
    )

def _get_column_info(data_frame: DataFrame, column_label: str) -> typing.List[ColumnInfo]:
    column_series: Series = data_frame[column_label]

    column_descriptive_statistics = column_series.describe()
    
    return ColumnInfo(
        column = Column(columnName = column_label, type = str(column_series.dtype)),
        descriptiveStatisticsFeatures = map(lambda feature_name: _map_feature(column_descriptive_statistics, feature_name), column_descriptive_statistics.keys())
    )

def _map_feature(column_descriptive_statistics: Series, feature_name: str) -> DescriptiveStatisticsFeature:
    feature_value = column_descriptive_statistics[feature_name]

    return DescriptiveStatisticsFeature(
        name = feature_name,
        value = str(feature_value),
        featureType = str(type(feature_value))
    )
