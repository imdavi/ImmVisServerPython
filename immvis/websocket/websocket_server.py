from tornado.websocket import WebSocketHandler
from websocket.actions.action import Action, ActionResult

from websocket.message_handler import MessageHandler

class ImmVisWebSocket(WebSocketHandler):

    def initialize(self, message_handler: MessageHandler):
        self.message_handler = message_handler

    def open(self):
        print("Someone has connected!")

    def on_close(self):
        print("Someone has disconnected!")

    def on_message(self, message):
        response = self.message_handler.handle_message(message)

        if response is not None:
            self.write_message(response)
