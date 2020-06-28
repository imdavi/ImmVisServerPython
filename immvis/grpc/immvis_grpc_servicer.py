
from .proto import immvis_pb2_grpc
from .proto.immvis_pb2 import AvailableDatasetsList, DatasetMetadata
from ..data.data_manager import DataManager
from .mappers import get_dataset_metadata, map_dataset_to_plot


class ImmvisGrpcServicer(immvis_pb2_grpc.ImmVisServicer):

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

    def GetDatasetToPlot(self, request, context):
        columns_to_plot = request.columnsNames

        dataset = self._data_manager.get_dataset_to_plot(columns_to_plot)

        return map_dataset_to_plot(dataset)
