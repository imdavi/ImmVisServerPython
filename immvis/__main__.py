from concurrent import futures
import time
import grpc
import immvis_pb2
import immvis_pb2_grpc
from immvisserver import ImmVisServer
from immvisdiscovery import ImmVisDiscoveryService

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

def start_server(data_frame=None):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    immvis_pb2_grpc.add_ImmVisServicer_to_server(ImmVisServer(data_frame), server)
    server.add_insecure_port('[::]:50051')
    server.start()

    discovery_service = ImmVisDiscoveryService()
    discovery_service.start()

    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    print("Running server...")
    start_server()
