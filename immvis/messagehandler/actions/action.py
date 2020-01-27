from abc import ABC, abstractmethod
from pandas import DataFrame
from messagehandler.actions.action_result import ActionResult


class Action(ABC):
    object_type: str

    @abstractmethod
    def process(self, data_frame: DataFrame) -> ActionResult:
        pass


class TransformAction(Action):
    @abstractmethod
    def process(self, data_frame: DataFrame) -> ActionResult:
        pass


