from websocket.actions.action import Action, TransformAction
from websocket.actions.action_result import ActionResult
from pandas import DataFrame
from abc import ABC


class DataStore():
    data_frame: DataFrame = None

    def run_action(self, action: Action) -> ActionResult:
        result = action.process(self.data_frame)

        if result is not None:
            if isinstance(action, TransformAction):
                if isinstance(result.data, DataFrame):
                    self.data_frame = result.data_frame
                else:
                    raise Exception(
                        'Results from transform must be a data_frame.')

        return result
