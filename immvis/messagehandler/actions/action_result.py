class ActionResult():
    data: object
    type_name: str

    def __init__(self, type_name: str,  data: object):
        self.data = data
        self.type_name = type_name
