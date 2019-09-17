from data.utils.dataset import open_dataset_file, get_data_frame_rows_as_list
from data.utils.outliers import map_outliers, supports_outliers_check
from data.utils.kmeans import get_kmeans_centroids, get_kmeans_clustering_mapping
from data.utils.exceptions import DatasetNotAvailable, DimensionNotAvailable, NoDimensionsAvailableToMapOutliers

class DataManager():
    data_frame = None

    def __init__(self, data_frame=None):
        self.data_frame = data_frame

    def _has_dimension(self, dimension_name):
        self._assert_dataset_was_loaded()
        return str(dimension_name) in self.data_frame

    def _assert_dimension_exists(self, dimension_name):
        if not self._has_dimension(dimension_name):
            raise DimensionNotAvailable

    def _assert_dataset_was_loaded(self):
        if self.data_frame is None:
            raise DatasetNotAvailable

    def load_dataset(self, file_path):
        if self.data_frame is not None:
            del self.data_frame

        self.data_frame = open_dataset_file(file_path)

    def remove_rows_with_missing_values(self):
        self.data_frame = self.data_frame.dropna()

    def remove_columns_with_missing_values(self):
        self.data_frame = self.data_frame.dropna(1)

    def get_dataset_dimensions(self):
        self._assert_dataset_was_loaded()

        for column in self.data_frame:
            yield (column, self.get_dimension_type(column))

    def get_dimension_type(self, dimension_name):
        self._assert_dimension_exists(dimension_name)

        return str(self.data_frame.dtypes[dimension_name])

    def get_dimension_descriptive_statistics(self, dimension_name):
        self._assert_dimension_exists(dimension_name)

        desc_stats = self.data_frame[dimension_name].describe()

        for feature_name in desc_stats.keys():
            feature_value = str(desc_stats[feature_name])
            feature_type = str(type(desc_stats[feature_name]))
            yield (feature_name, feature_value, feature_type)

    def get_dimension_values(self, dimension_name):
        self._assert_dimension_exists(dimension_name)

        dimension_series = self.data_frame[dimension_name]

        for _, value in dimension_series.iteritems():
            yield value

    def get_dataset_rows(self, selected_dimensions=None):
        self._assert_dataset_was_loaded()

        if selected_dimensions is None or len(selected_dimensions) == 0:
            selected_dimensions = self.data_frame.columns

        for dimension_name in selected_dimensions:
            self._assert_dimension_exists(dimension_name)

        return get_data_frame_rows_as_list(self.data_frame[selected_dimensions])

    def get_correlation_between_two_dimensions(self, dimension1, dimension2):
        self._assert_dimension_exists(dimension1)
        self._assert_dimension_exists(dimension2)

        series_dimension1 = self.data_frame[dimension1]
        series_dimension2 = self.data_frame[dimension2]

        return series_dimension1.corr(series_dimension2)

    def get_correlation_matrix(self):
        self._assert_dataset_was_loaded()

        correlation_matrix = self.data_frame.corr()

        return get_data_frame_rows_as_list(correlation_matrix)

    def get_outlier_mapping(self, dimensions_to_check=None):
        self._assert_dataset_was_loaded()

        if dimensions_to_check is None or len(dimensions_to_check) == 0:
            dimensions_to_check = self.data_frame.columns

        dimensions = list(
            filter(
                lambda dimension_name:
                self._has_dimension(dimension_name) and supports_outliers_check(self.get_dimension_type(dimension_name)),
                dimensions_to_check
            )
        )

        if len(dimensions) == 0:
            raise NoDimensionsAvailableToMapOutliers

        values = self.data_frame[dimensions].values

        outlier_mapping = map_outliers(values)

        for is_outlier in outlier_mapping:
            yield is_outlier

    def get_kmeans_centroids(self, n_clusters, selected_dimensions):
        self._assert_dataset_was_loaded()

        if selected_dimensions is None or len(selected_dimensions) == 0:
            selected_dimensions = self.data_frame.columns

        for dimension_name in selected_dimensions:
            self._assert_dimension_exists(dimension_name)

        return get_kmeans_centroids(n_clusters, self.data_frame[selected_dimensions])

    def get_kmeans_clustering_mapping(self, n_clusters, selected_dimensions):
        self._assert_dataset_was_loaded()

        if selected_dimensions is None or len(selected_dimensions) == 0:
            selected_dimensions = self.data_frame.columns

        for dimension_name in selected_dimensions:
            self._assert_dimension_exists(dimension_name)

        return get_kmeans_clustering_mapping(n_clusters, self.data_frame[selected_dimensions])
