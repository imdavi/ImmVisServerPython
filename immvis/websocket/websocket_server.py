from tornado.websocket import WebSocketHandler
from messagehandler.actions.action import Action, ActionResult
from messagehandler.message_handler import MessageHandler
from discovery.discovery_service import DiscoveryService

class ImmVisWebSocket(WebSocketHandler):

    def initialize(self, message_handler: MessageHandler, discovery_service: DiscoveryService):
        self.message_handler = message_handler
        self.discovery_service = discovery_service            

    def open(self):
        print("Someone has connected!")

        if self.discovery_service.is_running():
            self.discovery_service.stop()

    def on_close(self):
        print("Someone has disconnected!")

        if not self.discovery_service.is_running():
            self.discovery_service.start()

    def on_message(self, message):
        response = self.message_handler.handle_message(message)

        if response is not None:
            self.write_message(response)
