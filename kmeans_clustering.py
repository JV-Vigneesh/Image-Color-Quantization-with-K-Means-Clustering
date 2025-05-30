import numpy as np
from sklearn.cluster import MiniBatchKMeans
import multiprocessing


def _quantise_chunk(chunk, num_clusters):
    """Helper function for multiprocessing."""
    model = MiniBatchKMeans(n_clusters=num_clusters, random_state=0)
    labels = model.fit_predict(chunk)
    return model.cluster_centers_[labels]


class KMeansClustering:
    def __init__(self, num_clusters=8):
        self.num_clusters = num_clusters

    def fit(self, pixels):
        """
        Quantise pixels using MiniBatchKMeans with parallel processing.
        """
        cpu_count = multiprocessing.cpu_count()
        chunks = np.array_split(pixels, cpu_count)

        with multiprocessing.Pool(cpu_count) as pool:
            results = pool.starmap(_quantise_chunk, [(chunk, self.num_clusters) for chunk in chunks])

        quantised_pixels = np.vstack(results)
        return quantised_pixels
