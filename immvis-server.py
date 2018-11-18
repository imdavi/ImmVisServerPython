from concurrent import futures
import time
import grpc
import immvis_pb2
import immvis_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class ImmVisServer(immvis_pb2_grpc.ImmVisServicer):
    def OpenDatasetFile(self, request, content):
        print("Received request!" + request.filePath)
        return immvis_pb2.OpenDatasetFileResponse(responseCode=0)

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