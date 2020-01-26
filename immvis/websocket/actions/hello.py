from websocket.actions.action_result import ActionResult
from websocket.actions.action import Action
from pandas import DataFrame
from kim import field


class HelloAction(Action):
    def process(self, data_frame: DataFrame) -> ActionResult:
        return ActionResult('HelloAction', str.__name__)