

class ActionResult():
    data: object
    type_name: str

    def __init__(self, data: object, type_name: str):
        self.data = data
        self.type_name = type_name


EMPTY_RESULT = ActionResult(None, None)