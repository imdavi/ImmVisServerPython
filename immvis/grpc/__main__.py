from ..utils import common_constants as constants
from ._grpc_helper import create_server
from .immvis_grpc_server import ImmvisGrpcServer
from ..discovery import DiscoveryService
from time import sleep
from .proto import immvis_pb2_grpc
from .immvis_grpc_servicer import ImmvisGrpcServicer
import grpc

if __name__=='__main__':
    print("Creating ImmvisGrpcServicer")
    immvis_grpc_servicer = ImmvisGrpcServicer()

    print("Creating GRPC server...")
    grpc_server: grpc.Server = create_server()
    immvis_pb2_grpc.add_ImmVisServicer_to_server(immvis_grpc_servicer, grpc_server)

    print("Creating Discovery server...")
    discovery_service: DiscoveryService = DiscoveryService(debug=True)

    print("Creating ImmvisGrpcServer...")
    immvis_grpc_server:ImmvisGrpcServer = ImmvisGrpcServer(grpc_server, discovery_service)
    
    print("Starting ImmvisGrpcServer...")

    try:
        immvis_grpc_server.start()
        print("ImmvisGrpcServer has started!")
        while True:
            sleep(constants._ONE_DAY_IN_SECONDS)
    except (KeyboardInterrupt, SystemExit):
        print("Requested to stop ImmvisGrpcServer.")
        immvis_grpc_server.stop()
        print("ImmvisGrpcServer has stopped!")
    