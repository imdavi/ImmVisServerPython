from concurrent import futures
import time
import grpc
import pandas as pd
import pandas.api.types as ptypes
import immvis_pb2
import immvis_pb2_grpc
import numpy as np

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class ImmVisServer(immvis_pb2_grpc.ImmVisServicer):
    data_frame = None

    def OpenDatasetFile(self, request, content):
        file_path = request.filePath

        responseCode = 0

        try:
            if "csv" in file_path:
                self.data_frame = pd.read_csv(file_path)
            elif "json" in file_path:
                self.data_frame = pd.read_json(file_path)
            else:
                responseCode = 1
        except:
            responseCode = 2

        return immvis_pb2.OpenDatasetFileResponse(responseCode=responseCode)

    def GetDatasetDimensions(self, request, content):
        if self.data_frame is None:
            raise Exception("Failed to get dimensions.")

        types = self.data_frame.dtypes
        
        for column in self.data_frame:
            yield immvis_pb2.DimensionInfo(name=column, type=str(types[column]))

    def GetDimensionInfo(self, request, content):
        dimension_name = request.name

        dimension_series = self.data_frame[dimension_name]

        return str(dimension_series.dtype)
    
    def GetDimensionDescriptiveStatistics(self, request, content):
        dimension_name = request.name

        desc_stats = self.data_frame[dimension_name].describe()

        for feature_name in desc_stats.keys():
            feature_value = str(desc_stats[feature_name])
            feature_type = str(type(desc_stats[feature_name]))
            yield immvis_pb2.Feature(name=feature_name, value=feature_value, type=feature_type)
    
    def GetDimensionData(self, request_iterator, context):
        for dimension in request_iterator:
            dimension_name = dimension.name

            dimension_series = self.data_frame[dimension_name]

            dimension_type = str(dimension_series.dtype)

            dimension_data = [str(value) for value in dimension_series.values]

            yield immvis_pb2.DimensionData(name=dimension_name, type=dimension_type, data=dimension_data)
    def GetOutlierMapping(self, request_iterator, context):
        dimensions = [dimension.name for dimension in request_iterator]

        outlier_mapping = is_outlier(self.data_frame[dimensions].values)
                    
        dimension_name = "OutlierMapping"

        dimension_type = "bool"

        dimension_data = [str(value) for value in outlier_mapping]

        return immvis_pb2.DimensionData(name=dimension_name, type=dimension_type, data=dimension_data)

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
        points = points[:,None]
    median = np.median(points, axis=0)
    diff = np.sum((points - median)**2, axis=-1)
    diff = np.sqrt(diff)
    med_abs_deviation = np.median(diff)
    modified_z_score = 0.6745 * diff / med_abs_deviation
    return modified_z_score > thresh


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    immvis_pb2_grpc.add_ImmVisServicer_to_server(ImmVisServer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ ==   '__main__':
    serve()