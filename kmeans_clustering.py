import numpy as np
from sklearn.cluster import MiniBatchKMeans


class KMeansClustering:
    def __init__(self, num_clusters=8):
        self.num_clusters = num_clusters

    def fit(self, pixels):
        """
        Quantise pixels using MiniBatchKMeans trained on a sampled subset.
        """
        pixels = pixels.reshape(-1, 3)
        sample_size = min(10000, len(pixels))
        sample_indices = np.random.choice(len(pixels), size=sample_size, replace=False)
        sample_pixels = pixels[sample_indices]

        model = MiniBatchKMeans(n_clusters=self.num_clusters, random_state=42)
        model.fit(sample_pixels)

        labels = model.predict(pixels)
        quantised_pixels = model.cluster_centers_[labels]

        return quantised_pixels
