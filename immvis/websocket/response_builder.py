from websocket.actions.action import Action
from websocket.actions.action_result import ActionResult
import json
import numpy as np
from data.utils.dataset import get_data_frame_rows_as_list
from pandas import DataFrame


_FIELD_TYPE = 'type'
_FIELD_TYPE_NAME = 'type_name'
_FIELD_DATA = 'data'
_FIELD_CAUSE = 'cause'
_FIELD_VALUE = 'value'
_FIELD_MESSAGE = 'message'
_FIELD_COLUMNS = 'columns'
_FIELD_COLUMNS_TYPES = 'columns_types'
_FIELD_ACTION = 'action'

_TYPE_ERROR = 'error'
_TYPE_RESPONSE = 'response'


def build_response_from_action_result(action_result: ActionResult, source_action: Action = None) -> str:
    return _to_json_str({
        _FIELD_TYPE: _TYPE_RESPONSE,
        _FIELD_ACTION: source_action.object_type,
        _FIELD_DATA: _build_data_field(action_result)
    })


def _build_data_field(action_result: ActionResult):
    data_obj = {
        _FIELD_TYPE_NAME: action_result.type_name
    }

    if type(action_result.data) is DataFrame:
        data_frame: DataFrame = action_result.data

        data_obj[_FIELD_VALUE] = list(get_data_frame_rows_as_list(data_frame))
        data_obj[_FIELD_COLUMNS] = list(map(
            lambda column: str(column), data_frame.columns))
        data_obj[_FIELD_COLUMNS_TYPES] = list(map(
            lambda type: str(type), data_frame.dtypes))
    else:
        data_obj[_FIELD_VALUE] = action_result.data

    return data_obj


def build_response_from_error(error: Exception) -> str:
    error_obj = {
        _FIELD_CAUSE: error.__class__.__name__
    }

    message = error.args[0]

    if message is not None:
        error_obj[_FIELD_MESSAGE] = str(message)

    return _to_json_str(error_obj)


def _wrap_message(message_type: str, message_data: object):
    return {
        _FIELD_TYPE: message_type,
        _FIELD_DATA: message_data
    }


def _to_json_str(message_object: object):
    return json.dumps(message_object, cls=ImmVisJsonEncoder)


class ImmVisJsonEncoder(json.JSONEncoder):
    def default(self, obj):  # pylint: disable=E0202
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
