from websocket.actions.action_result import ActionResult
from websocket.actions.action import TransformAction
from pandas import DataFrame
from kim import field
from data.utils.dataset import open_dataset_file


class LoadDataFrameFromFile(TransformAction):
    file_path: str

    def process(self, data_frame: DataFrame) -> ActionResult:
        data_frame = open_dataset_file(self.file_path)

        return ActionResult(data_frame, DataFrame.__name__)
