from time import sleep
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST, gethostbyname, gethostname
from string import Template
from concurrent import futures
import time

_MAGIC = "U2bhY3XUOli9GgdUGs9ruxuXKpuj78Qi3zNT5IEkiQy5ex4UxqXZ5ZDAj9vkTyVz2GZiFXDS4bY5Ayve2HrAiB7G2jN7d5rskERyj3b5GeQAv1PYEOdD5sys"
_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class ImmVisDiscoveryService():
    _SHOULD_BROADCAST = True
    _port = None
    _delay = None
    _magic = None
    _executor = futures.ThreadPoolExecutor(max_workers=2)

    def __init__(self, port=5000, delay=5, magic=_MAGIC):
        self._port = port
        self._delay = delay
        self._magic = magic

    def start(self):
        self._executor.submit(self.__broadcast)

    def __broadcast(self):
        broadcast_socket = socket(AF_INET, SOCK_DGRAM)
        broadcast_socket.bind(('', 0))
        broadcast_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        current_ip = gethostbyname(gethostname())

        while self._SHOULD_BROADCAST:
            data = Template("$magic:$ip").substitute(
                magic=_MAGIC, ip=current_ip)
            broadcast_socket.sendto(str.encode(data), ('<broadcast>', self._port))
            print("Sending service announcement with ip:" + current_ip)
            time.sleep(self._delay)

        return

    def stop(self):
        self._SHOULD_BROADCAST = False
        self._executor.shutdown()

if __name__ == '__main__':
    print("Running service discovery...")
    discovery_service = ImmVisDiscoveryService()
    discovery_service.start()

    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        discovery_service.stop()

