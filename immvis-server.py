from concurrent import futures
import time
import grpc
import pandas as pd
import pandas.api.types as ptypes
import immvis_pb2
import immvis_pb2_grpc

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

    def GetDimensionFloatValues(self, request, content):
        dimension_name = request.name
        
        dimension_series = self.data_frame[dimension_name]
        
        is_float_dimension = ptypes.is_float_dtype(dimension_series)

        if not is_float_dimension:
            raise Exception("The type of the dimension '" + dimension_name + "is not float.")

        for value in dimension_series:
            yield immvis_pb2.FloatDimensionValue(value=value)

    def GetDimensionFloatHead(self, request, content):
        dimension_name = request.name
        
        dimension_series = self.data_frame[dimension_name]
        
        is_float_dimension = ptypes.is_float_dtype(dimension_series)

        if not is_float_dimension:
            raise Exception("The type of the dimension '" + dimension_name + "is not float.")

        for value in dimension_series.head():
            yield immvis_pb2.FloatDimensionValue(value=value)

    def GetDimensionFloatTail(self, request, content):
        dimension_name = request.name
        
        dimension_series = self.data_frame[dimension_name]
        
        is_float_dimension = ptypes.is_float_dtype(dimension_series)

        if not is_float_dimension:
            raise Exception("The type of the dimension '" + dimension_name + "is not float.")

        for value in dimension_series.tail():
            yield immvis_pb2.FloatDimensionValue(value=value)

    def GetDimensionStringValues(self, request, content):
        dimension_name = request.name
        
        dimension_series = self.data_frame[dimension_name]
        
        is_string_dimension = ptypes.is_string_dtype(dimension_series)

        if not is_string_dimension:
            raise Exception("The type of the dimension '" + dimension_name + "is not float.")

        for value in dimension_series:
            yield immvis_pb2.StringDimensionValue(value=value)
    
    def GetDimensionDescriptiveStatistics(self, request, content):
        dimension_name = request.name

        desc_stats = self.data_frame[dimension_name].describe()

        for feature_name in desc_stats.keys():
            feature_value = str(desc_stats[feature_name])
            feature_type = str(type(desc_stats[feature_name]))
            yield immvis_pb2.Feature(name=feature_name, value=feature_value, type=feature_type)

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