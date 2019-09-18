from concurrent import futures

import grpc
from proto import immvis_pb2_grpc
from rpc.grpc_servicer import GrpcServicer
from discovery.discovery_service import DiscoveryService

class ImmVisServer():

    _server = None
    _discovery_service = None

    def __init__(self, grpc_server_port=50051, discovery_port=5000, data_manager=None):
        self._server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        immvis_pb2_grpc.add_ImmVisServicer_to_server(GrpcServicer(data_manager), self._server)
        self._server.add_insecure_port('[::]:' + str(grpc_server_port))
        self._discovery_service = DiscoveryService(port=discovery_port)

    def start(self):
        self._server.start()
        self._discovery_service.start()

    def stop(self):
        self._server.stop(0)
        self._discovery_service.stop()
