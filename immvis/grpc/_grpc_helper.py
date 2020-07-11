import grpc
from concurrent import futures

_MAX_RECEIVE_MESSAGE_LENGTH = 100 * 1024 * 1024
_THREAD_POOL_EXECUTOR_MAX_WORKERS = 10
_SERVER_PORT = 50051


def create_server(server_port: int = _SERVER_PORT, max_receive_message_length=_MAX_RECEIVE_MESSAGE_LENGTH) -> grpc.Server:
    server: grpc.Server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=_THREAD_POOL_EXECUTOR_MAX_WORKERS),
        options=[("grpc.max_receive_message_length", max_receive_message_length)],
    )
    server.add_insecure_port('[::]:' + str(server_port))
    return server
