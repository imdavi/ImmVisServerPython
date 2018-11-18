from concurrent import futures
import time
import grpc
import pandas as pd
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