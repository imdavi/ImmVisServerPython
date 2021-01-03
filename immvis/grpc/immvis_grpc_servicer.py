
from .proto import immvis_pb2_grpc
from .proto.immvis_pb2 import AvailableDatasetsList, DatasetMetadata, NormalisedDataset, NormalisedRow
from ..data.data_manager import DataManager
from .mappers import get_dataset_metadata


class ImmvisGrpcServicer(immvis_pb2_grpc.ImmVisPandasServicer):

    _data_manager:DataManager = None

    def __init__(self, data_manager: DataManager):
        self._data_manager = data_manager

    def ListAvailableDatasets(self, request, context):
        available_datasets = self._data_manager.list_available_datasets()
        return AvailableDatasetsList(datasetsPaths = available_datasets)

    def LoadDataset(self, request, context):
        dataset_path = request.datasetPath

        dataset = self._data_manager.load_dataset(dataset_path)
        
        return get_dataset_metadata(dataset)

    def GetNormalisedDataset(self, request, context):
        columns_names = request.columnsNames

        normalised_data_frame = self._data_manager.get_normalised_dataset(columns_names)

        return NormalisedDataset(rows=list(map(lambda row: NormalisedRow(values=row), normalised_data_frame.values)))

    def GenerateDataset(self, request, context):
        columns_amount = request.columnsAmount
        rows_amount = request.rowsAmount
        centers_amount = request.centersAmount

        dataset = self._data_manager.generate_dataset(columns_amount, rows_amount, centers_amount)

        return get_dataset_metadata(dataset)
