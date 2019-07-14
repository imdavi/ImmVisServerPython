from concurrent import futures
import time
import grpc
import pandas as pd
import pandas.api.types as ptypes
import immvis_pb2
import immvis_pb2_grpc
import numpy as np
from sklearn.cluster import KMeans
import filetype
from _extutils import is_csv, is_excel, is_image, is_json
from _imgdataset import read_image_as_dataframe

ERROR_CODE_UNKNOWN_EXTENSION = 1
ERROR_CODE_CANNOT_OPEN_FILE = 2
RETURN_CODE_SUCCESS = 0

class ImmVisGrpcServer(immvis_pb2_grpc.ImmVisServicer):
    data_frame = None

    def __init__(self, data_frame = None):
        self.data_frame = data_frame

    def _assertDimensionExists(self, dimension_name):
        if not str(dimension_name) in self.data_frame:
            raise Exception("The dimension \'" + dimension_name +
                            "doesn't exist at the dataset.")

    def _assertLoadedDataset(self):
        if self.data_frame is None:
            raise Exception("Failed to get dimensions.")

    def OpenDatasetFile(self, request, context):
        file_path = request.filePath.strip()

        print("Trying to open the file '" + file_path + "'...")

        responseCode = RETURN_CODE_SUCCESS

        try:
            if is_csv(file_path):
                self.data_frame = pd.read_csv(file_path)
            elif is_json(file_path):
                self.data_frame = pd.read_json(file_path)
            elif is_excel(file_path):
                self.data_frame = pd.read_excel(file_path)
            elif is_image(file_path):
                self.data_frame = read_image_as_dataframe(file_path)
            else:
                responseCode = ERROR_CODE_UNKNOWN_EXTENSION
        except Exception as exception:
            print("Error during opening the file: '" + type(exception) + "'")
            responseCode = ERROR_CODE_CANNOT_OPEN_FILE

        if responseCode is 0:
            print("Loaded file with success")
            self.data_frame = self.data_frame.dropna().dropna(1)
        else:
            print("File was not loaded. Error code: " + str(responseCode))

        return immvis_pb2.OpenDatasetFileResponse(responseCode=responseCode)

    def GetDatasetDimensions(self, request, context):
        if self.data_frame is None:
            raise Exception("Failed to get dimensions.")

        types = self.data_frame.dtypes

        for column in self.data_frame:
            yield immvis_pb2.DimensionInfo(name=column, type=str(types[column]))

    def GetDimensionInfo(self, request, context):
        dimension_name = request.name

        dimension_series = self.data_frame[dimension_name]

        return str(dimension_series.dtype)

    def GetDimensionDescriptiveStatistics(self, request, context):
        dimension_name = request.name

        desc_stats = self.data_frame[dimension_name].describe()

        for feature_name in desc_stats.keys():
            feature_value = str(desc_stats[feature_name])
            feature_type = str(type(desc_stats[feature_name]))
            yield immvis_pb2.Feature(name=feature_name, value=feature_value, type=feature_type)

    def GetDimensionData(self, request_iterator, context):
        for dimension in request_iterator:
            dimension_name = dimension.name

            dimension_data = None

            if dimension_name is "":
                dimension_data = immvis_pb2.DimensionData(
                    name="empty", type="empty", data=[])
            else:
                dimension_series = self.data_frame[dimension_name]

                dimension_type = str(dimension_series.dtype)

                dimension_data = [str(value)
                                  for value in dimension_series.values]

                dimension_data = immvis_pb2.DimensionData(
                    name=dimension_name, type=dimension_type, data=dimension_data)

            yield dimension_data

    def GetOutlierMapping(self, request_iterator, context):
        dimensions = [dimension.name for dimension in request_iterator if dimension.name !=
                      "" and supportsOutliers(str(self.data_frame[dimension.name].dtype))]

        outlier_mapping = is_outlier(self.data_frame[dimensions].values)

        dimension_name = "OutlierMapping"

        dimension_type = "bool"

        dimension_data = []

        if len(dimensions) > 0:
            dimension_data = [str(value) for value in outlier_mapping]
        else:
            dimension_data = [False for x in range(
                0, len(self.data_frame.index))]

        return immvis_pb2.DimensionData(name=dimension_name, type=dimension_type, data=dimension_data)

    def GetKMeansCentroids(self, request, context):
        numClusters = request.numClusters

        dimensions = [dimension.name for dimension in request.dimensions]

        kmeans = create_k_means(numClusters)

        kmeans.fit(self.data_frame[dimensions])

        for cluster_center in kmeans.cluster_centers_:
            coordinates = [str(value) for value in cluster_center]
            yield immvis_pb2.KMeansCentroid(type='float64', coordinates=coordinates)

    def GetKMeansClusterMapping(self, request, context):
        numClusters = request.numClusters

        dimensions = [dimension.name for dimension in request.dimensions]

        kmeans = create_k_means(numClusters)

        kmeans.fit_transform(self.data_frame[dimensions])

        dimension_name = "KMeansClusteringMapping"

        dimension_type = "int64"

        dimension_data = []

        if len(dimensions) > 0:
            dimension_data = [str(value) for value in kmeans.labels_]
        else:
            dimension_data = [0 for x in range(0, len(self.data_frame.index))]

        return immvis_pb2.DimensionData(name=dimension_name, type=dimension_type, data=dimension_data)

    def GetDatasetValues(self, request, context):
        self._assertLoadedDataset()

        for index, row in enumerate(self.data_frame.values):
            row_values_list = row.tolist()

            row_values_str_list = map(
                lambda value: str(value), row_values_list)

            yield immvis_pb2.DataRow(index=index, values=row_values_str_list)

    def GetCorrelationBetweenTwoDimensions(self, request, context):
        self._assertLoadedDataset()

        dimension1 = request.dimension1.name
        self._assertDimensionExists(dimension1)

        dimension2 = request.dimension2.name
        self._assertDimensionExists(dimension2)

        correlation = self.data_frame[dimension1].corr(
            self.data_frame[dimension2])

        return immvis_pb2.FloatResult(result=correlation)

    def GetCorrelationMatrix(self, request, context):
        self._assertLoadedDataset()

        correlation_matrix = self.data_frame.corr()

        for index, row in enumerate(correlation_matrix.values):
            row_values_list = row.tolist()

            row_values_str_list = map(
                lambda value: str(value), row_values_list)

            yield immvis_pb2.DataRow(index=index, values=row_values_str_list)


def create_k_means(numClusters):
    return KMeans(n_clusters=numClusters, init='random')


def supportsOutliers(dimension_name):
    return dimension_name != "object" and dimension_name != "int64" and dimension_name != ""


def is_outlier(points, thresh=3.5):
    """
    Returns a boolean array with True if points are outliers and False 
    otherwise.

    Parameters:
    -----------
        points : An numobservations by numdimensions array of observations
        thresh : The modified z-score to use as a threshold. Observations with
            a modified z-score (based on the median absolute deviation) greater
            than this value will be classified as outliers.

    Returns:
    --------
        mask : A numobservations-length boolean array.

    References:
    ----------
        Boris Iglewicz and David Hoaglin (1993), "Volume 16: How to Detect and
        Handle Outliers", The ASQC Basic References in Quality Control:
        Statistical Techniques, Edward F. Mykytka, Ph.D., Editor. 
    """
    if len(points.shape) == 1:
        points = points[:, None]
    median = np.median(points, axis=0)
    diff = np.sum((points - median)**2, axis=-1)
    diff = np.sqrt(diff)
    med_abs_deviation = np.median(diff)
    modified_z_score = 0.6745 * diff / med_abs_deviation
    return modified_z_score > thresh
