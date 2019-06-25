from time import sleep
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST, gethostbyname, gethostname
from string import Template
import asyncio

_PORT = 5000
_MAGIC = "U2bhY3XUOli9GgdUGs9ruxuXKpuj78Qi3zNT5IEkiQy5ex4UxqXZ5ZDAj9vkTyVz2GZiFXDS4bY5Ayve2HrAiB7G2jN7d5rskERyj3b5GeQAv1PYEOdD5sys"

_BROADCAST_DELAY = 5

class ServiceDiscovery():
    _SHOULD_BROADCAST = True
    async def start_broadcast(self):
        broadcast_socket = socket(AF_INET, SOCK_DGRAM)
        broadcast_socket.bind(('', 0))
        broadcast_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        current_ip = gethostbyname(gethostname())

        while self._SHOULD_BROADCAST:
            data = Template("$magic:$ip").substitute(magic=_MAGIC, ip=current_ip)
            broadcast_socket.sendto(str.encode(data), ('<broadcast>', _PORT))
            print("Sending service announcement with ip:" + current_ip)
            await asyncio.sleep(_BROADCAST_DELAY)
        
        return
    
    def stop_broadcast(self):
        self._SHOULD_BROADCAST = False

async def start_service_discovery():
    print("Running service discovery...")
    service_discovery = ServiceDiscovery()
    await service_discovery.start_broadcast()
