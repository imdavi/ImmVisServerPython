from rpc.grpc_server import ImmVisServer
from time import sleep

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

_immvis_server = ImmVisServer()

def start_server(data_frame=None):
    print("Server has started!")
    _immvis_server.start()

    try:
        while True:
            sleep(_ONE_DAY_IN_SECONDS)
    except (KeyboardInterrupt, SystemExit):
        stop_server()

def stop_server():
    print("Server has stopped!")
    _immvis_server.stop()

if __name__ == '__main__':
    print("Running server...")
    start_server()