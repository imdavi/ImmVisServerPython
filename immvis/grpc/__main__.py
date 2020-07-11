from ..utils import common_constants as constants
from ..discovery import DiscoveryService
from time import sleep
from .proto import immvis_pb2_grpc
from .immvis_grpc_servicer import ImmvisGrpcServicer
from ..data import DataManager
from ._grpc_helper import create_server
import grpc

if __name__=='__main__':
    print("Creating DataManager")
    data_manager = DataManager()

    print("Creating ImmvisGrpcServicer")
    immvis_grpc_servicer = ImmvisGrpcServicer(data_manager)

    print("Creating GRPC server...")
    server: grpc.Server = create_server()
    immvis_pb2_grpc.add_ImmVisPandasServicer_to_server(immvis_grpc_servicer, server)

    print("Creating Discovery server...")
    discovery_service: DiscoveryService = DiscoveryService(debug=True)

    print("Starting ImmvisGrpcServer...")

    try:
        discovery_service.start()
        server.start()
        print("ImmvisGrpcServer has started!")
        server.wait_for_termination()
        while True:
            sleep(constants._ONE_DAY_IN_SECONDS)
    except (KeyboardInterrupt, SystemExit):
        print("Requested to stop ImmvisGrpcServer.")
        discovery_service.stop()
        print("ImmvisGrpcServer has stopped!")
    