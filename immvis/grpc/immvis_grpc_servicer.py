
from .proto import immvis_pb2_grpc
from .proto.immvis_pb2 import AvailableDatasetsList, DatasetMetadata, NormalisedDataset, NormalisedRow, ColumnsLabels, KMeansAnalysisResponse
from ..data.data_manager import DataManager
from .mappers import get_dataset_metadata, map_to_k_means_analysis_response


class ImmvisGrpcServicer(immvis_pb2_grpc.ImmVisPandasServicer):

    _data_manager: DataManager = None

    def __init__(self, data_manager: DataManager):
        self._data_manager = data_manager

    def ListAvailableDatasets(self, request, context):
        available_datasets = self._data_manager.list_available_datasets()
        return AvailableDatasetsList(datasetsPaths=available_datasets)

    def LoadDataset(self, request, context):
        dataset_path = request.datasetPath

        dataset = self._data_manager.load_dataset(dataset_path)

        return get_dataset_metadata(dataset)

    def GetNormalisedDataset(self, request, context):
        columns_names = request.columnsNames

        normalised_data_frame = self._data_manager.get_normalised_dataset(
            columns_names)

        return NormalisedDataset(
            columnsNames=columns_names,
            rows=list(map(lambda row: NormalisedRow(
                values=row), normalised_data_frame.values)),
            columnsLabels=list(map(lambda labels: ColumnsLabels(
                labels=labels), self._data_manager.get_columns_labels(columns_names)))
        )

    def GenerateDataset(self, request, context):
        columns_amount = request.columnsAmount
        rows_amount = request.rowsAmount
        centers_amount = request.centersAmount

        dataset = self._data_manager.generate_dataset(
            columns_amount, rows_amount, centers_amount)

        return get_dataset_metadata(dataset)

    def DoKMeansAnalysis(self, request, context):
        clusters_number = request.clustersNumber
        columns_names = request.columnsNames

        k_means_analysis_result = self._data_manager.do_kmeans_analysis(
            columns_names, clusters_number)

        labels_mapping = k_means_analysis_result.labels_mapping
        labels_mapping_labels = k_means_analysis_result.labels_mapping_labels
        centroids = k_means_analysis_result.centroids

        columns_labels = list(map(lambda labels: ColumnsLabels(
            labels=labels), labels_mapping_labels))

        return KMeansAnalysisResponse(
            labelsMapping=NormalisedDataset(
                columnsNames=labels_mapping.columns,
                rows=list(map(lambda row: NormalisedRow(
                    values=row), labels_mapping.values)),
                columnsLabels=columns_labels
            ),
            centroids=NormalisedDataset(
                columnsNames=centroids.columns,
                rows=list(map(lambda row: NormalisedRow(
                    values=row), centroids.values)),
                columnsLabels=columns_labels
            ),
        )
