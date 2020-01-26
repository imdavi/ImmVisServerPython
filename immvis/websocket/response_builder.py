from websocket.actions.action import Action
from websocket.actions.action_result import ActionResult
import json
import numpy as np
from data.utils.dataset import get_data_frame_rows_as_list


_FIELD_TYPE = 'type'
_FIELD_DATA = 'data'
_FIELD_CAUSE = 'cause'
_FIELD_MESSAGE = 'message'
_FIELD_COLUMNS = 'columns'
_FIELD_COLUMNS_TYPES = 'columns_types'

_TYPE_ERROR = 'error'
_TYPE_INFER = 'infer'
_TYPE_TRANSFORM = 'transform'


def build_response_from_action_result(action_result: ActionResult, source_action: Action = None) -> str:
    return {}

    # if isinstance(message_data, DataFrame):
    #     message_obj[_FIELD_COLUMNS] = map(
    #         lambda column: str(column), message_data.columns)
    #     message_obj[_FIELD_COLUMNS_TYPES] = map(
    #         lambda type: str(type), message_data.dtypes)


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
