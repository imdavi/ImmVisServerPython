from websocket.actions.action_result import ActionResult
from websocket.message_parser import MessageParser
from websocket.data_store import DataStore
from websocket.response_builder import build_response_from_action_result, build_response_from_error


class MessageHandler():

    def __init__(self, message_parser: MessageParser, data_store: DataStore):
        self.message_parser = message_parser
        self.data_store = data_store

    def handle_message(self, message: str) -> str:
        response = None

        try:
            action = self.message_parser.parse_json(message)

            result = self.data_store.run_action(action)

            response = build_response_from_action_result(result, action)

        except Exception as exception:
            response = build_response_from_error(exception)

        return response
