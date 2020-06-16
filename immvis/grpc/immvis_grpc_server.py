from ..discovery import DiscoveryService
import grpc

class ImmvisGrpcServer():
    _discovery_service: DiscoveryService = None
    _grpc_server: grpc.Server = None

    def __init__(self, grpc_server: grpc.Server, discovery_service: DiscoveryService):
        self._grpc_server = grpc_server
        self._discovery_service = discovery_service

    def start(self):
        self._discovery_service.start()

    def stop(self):
        self._discovery_service.stop()
