from ..proto.immvis_pb2 import KMeansAnalysisResponse, NormalisedDataset
from pandas import DataFrame

def map_to_k_means_analysis_response(k_means_analysis_result) -> KMeansAnalysisResponse:
    return KMeansAnalysisResponse(
        labelsMapping=_map_to_data_frame(labels_mapping),
        centroids=_map_to_data_frame(centroids)
    )

def _map_to_data_frame(data_frame: DataFrame) -> NormalisedDataset:
    pass
