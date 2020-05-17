
from .proto import immvis_pb2, immvis_pb2_grpc
from ..data import DataManager, UnknownDatasetType

ERROR_CODE_UNKNOWN_EXTENSION = 1
ERROR_CODE_CANNOT_OPEN_FILE = 2
RETURN_CODE_SUCCESS = 0

class GrpcServicer(immvis_pb2_grpc.ImmVisServicer):
    data_manager = None

    def __init__(self, data_manager = None):
        self.data_manager = data_manager or DataManager()

    def OpenDatasetFile(self, request, context):
        file_path = request.filePath.strip()

        print("Trying to open the file '" + file_path + "'...")

        responseCode = RETURN_CODE_SUCCESS

        try:
            self.data_manager.load_dataset(file_path)
        except UnknownDatasetType as exception:
            print("Error during opening the file: '" + type(exception) + "'")
            responseCode = ERROR_CODE_UNKNOWN_EXTENSION
        except Exception as exception:
            print("Error during opening the file: '" + type(exception) + "'")
            responseCode = ERROR_CODE_CANNOT_OPEN_FILE

        if responseCode is 0:
            print("Loaded file with success")
            self.data_manager.remove_rows_with_missing_values()
            self.data_manager.remove_columns_with_missing_values()
        else:
            print("File was not loaded. Error code: " + str(responseCode))

        return immvis_pb2.OpenDatasetFileResponse(responseCode=responseCode)

    def GetDatasetDimensions(self, request, context):
        dimensions = self.data_manager.get_dataset_dimensions()

        for dimension in dimensions:
            yield immvis_pb2.DimensionInfo(name=dimension[0], type=dimension[1])

    def GetDimensionInfo(self, request, context):
        dimension_name = request.name

        return self.data_manager.get_dimension_type(dimension_name)

    def GetDimensionDescriptiveStatistics(self, request, context):
        dimension_name = request.name

        desc_stats = self.data_manager.get_dimension_descriptive_statistics(dimension_name)

        for feature in desc_stats:
            feature_name = feature[0]
            feature_value = feature[1]
            feature_type = feature[2]
            yield immvis_pb2.Feature(name=feature_name, value=feature_value, type=feature_type)

    def GetDimensionData(self, request_iterator, context):
        for dimension in request_iterator:
            dimension_name = dimension.name

            dimension_data = None

            if dimension_name is "":
                dimension_data = immvis_pb2.DimensionData(
                    name="empty", type="empty", data=[])
            else:
                dimension_values = self.data_manager.get_dimension_values(dimension_name)

                dimension_type = self.data_manager.get_dimension_type(dimension_name)

                dimension_data = [str(value)
                                  for value in dimension_values]

                dimension_data = immvis_pb2.DimensionData(
                    name=dimension_name, type=dimension_type, data=dimension_data)

            yield dimension_data

    def GetOutlierMapping(self, request_iterator, context):
        dimensions = [dimension.name for dimension in request_iterator]

        outlier_mapping = self.data_manager.get_outlier_mapping(dimensions)

        dimension_name = "OutlierMapping"

        dimension_type = "bool"

        dimension_data = [str(value) for value in outlier_mapping]

        return immvis_pb2.DimensionData(name=dimension_name, type=dimension_type, data=dimension_data)

    def GetKMeansCentroids(self, request, context):
        numClusters = request.numClusters

        dimensions = [dimension.name for dimension in request.dimensions]

        centroids = self.data_manager.get_kmeans_centroids(numClusters, dimensions)

        for centroid in centroids:
            coordinates = [str(value) for value in centroid]
            yield immvis_pb2.KMeansCentroid(type='float64', coordinates=coordinates)

    def GetKMeansClusterMapping(self, request, context):
        numClusters = request.numClusters

        dimensions = [dimension.name for dimension in request.dimensions]

        clustering_mapping = self.data_manager.get_kmeans_centroids(numClusters, dimensions)

        dimension_name = "KMeansClusteringMapping"

        dimension_type = "int64"

        dimension_data = map(lambda value: str(value), clustering_mapping)

        return immvis_pb2.DimensionData(name=dimension_name, type=dimension_type, data=dimension_data)

    def GetDatasetValues(self, request_iterator, context):
        # dimensions = [dimension.name for dimension in request_iterator]

        rows = self.data_manager.get_dataset_rows()

        for index, row in enumerate(rows):
            row_values_str_list = map(
                lambda value: str(value), row)

            yield immvis_pb2.DataRow(index=index, values=row_values_str_list)

    def GetCorrelationBetweenTwoDimensions(self, request, context):
        dimension1 = request.dimension1.name

        dimension2 = request.dimension2.name

        correlation = self.data_manager.get_correlation_between_two_dimensions(dimension1,dimension2)

        return immvis_pb2.FloatResult(result=correlation)

    def GetCorrelationMatrix(self, request, context):
        correlation_matrix = self.data_manager.get_correlation_matrix()

        for index, row in enumerate(correlation_matrix):
            row_values_str_list = map(
                lambda value: str(value), row)

            yield immvis_pb2.DataRow(index=index, values=row_values_str_list)
