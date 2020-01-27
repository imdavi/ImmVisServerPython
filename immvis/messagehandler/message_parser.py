import json

from messagehandler.actions.action import Action
from messagehandler.actions.action_mapper import ActionMapper

class MessageParser():

    def parse_json(self, json_str: str) -> Action:
        parsed_message = json.loads(json_str)

        mapper = ActionMapper(data = parsed_message)

        return mapper.marshal()
