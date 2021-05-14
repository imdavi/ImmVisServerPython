from pandas import DataFrame
import typing
from .normalise_data_frame import normalise_data_frame
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from .get_columns_labels import get_columns_labels

class KMeansAnalysisResult():
    labels_mapping: DataFrame = None
    labels_mapping_labels: typing.List[typing.List[str]] = None
    centroids: DataFrame = None

    def __init__(self, labels_mapping: DataFrame, labels_mapping_labels: typing.List[typing.List[str]], centroids: DataFrame):
        self.labels_mapping = labels_mapping
        self.labels_mapping_labels = labels_mapping_labels
        self.centroids = centroids

def do_kmeans_analysis(data_frame: DataFrame, clusters_number: int) -> KMeansAnalysisResult:
    k_means: KMeans = None

    if clusters_number > 0:
        k_means = KMeans(n_clusters=clusters_number)
    else:
        k_means = KMeans()

    labels_mapping = normalise_data_frame(data_frame.iloc[:, : 3])
    columns = labels_mapping.columns

    k_means.fit_transform(labels_mapping)

    labels_mapping['Label'] = MinMaxScaler().fit_transform(k_means.labels_.reshape(-1,1))

    centroids = DataFrame(data=k_means.cluster_centers_, columns=columns)

    return KMeansAnalysisResult(labels_mapping=labels_mapping, labels_mapping_labels=get_columns_labels(data_frame, columns), centroids=centroids)
