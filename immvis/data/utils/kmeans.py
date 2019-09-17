from sklearn.cluster import KMeans


def _create_k_means(n_clusters, init='random'):
    return KMeans(n_clusters=n_clusters, init=init)

def get_kmeans_centroids(n_clusters, data_frame):
    kmeans = _create_k_means(n_clusters)

    kmeans.fit_transform(data_frame)

    for cluster_center in kmeans.cluster_centers_:
        yield cluster_center

def get_kmeans_clustering_mapping(n_clusters, data_frame):
    kmeans = _create_k_means(n_clusters)

    kmeans.fit_transform(data_frame)

    for label in kmeans.labels_: 
        yield label
