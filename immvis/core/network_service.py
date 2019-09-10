from service import Service
import abc

class NetworkService(Service):
    def __init__(self, port):
        self.port = port

    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def stop(self):
        pass