

class DimensionNotAvailable(Exception):
    pass

class DatasetNotAvailable(Exception):
    pass

class DataManager():
    data_frame = None

    def __init__(self, data_frame = None):
        self.data_frame = data_frame

    def _assert_dimension_exists(self, dimension_name):
        if not str(dimension_name) in self.data_frame:
            raise DimensionNotAvailable

    def _assert_dataset_was_loaded(self):
        if self.data_frame is None:
            raise DatasetNotAvailable
