import faiss
import numpy as np
from typing import List, Dict, Tuple
import os
import pickle
from loguru import logger

class FaissVectorStore:
    def __init__(self, dimension: int):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.metadata: List[Dict] = []

        logger.info(f"FAISS index initialized with dimension={dimension}")

    def add(self, vectors: np.ndarray, metadata: List[Dict]) -> None:
        if vectors.ndim != 2 or vectors.shape[1] != self.dimension:
            raise ValueError(
                f"Vector dimension mismatch. Expected {self.dimension}, got {vectors.shape}"
            )

        if len(vectors) != len(metadata):
            raise ValueError("Vectors and metadata length must match.")

        self.index.add(vectors.astype("float32"))
        self.metadata.extend(metadata)

        logger.info(
            f"Added {len(vectors)} vectors. Total index size={self.index.ntotal}"
        )

    def search(
        self,
        query_vector: np.ndarray,
        top_k: int
    ) -> List[Tuple[float, Dict]]:
        """
        Search top_k nearest vectors.
        Returns list of (distance, metadata)
        """

        if query_vector.ndim == 1:
            query_vector = query_vector.reshape(1, -1)

        if query_vector.shape[1] != self.dimension:
            raise ValueError(
                f"Query vector dimension mismatch. "
                f"Expected {self.dimension}, got {query_vector.shape}"
            )

        distances, indices = self.index.search(
            query_vector.astype("float32"), top_k
        )

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx == -1:
                continue
            results.append((float(dist), self.metadata[idx]))

        logger.info(f"Search completed. Returned top_k={top_k}")

        return results

    def save(self, directory: str) -> None:
        """
        Persist FAISS index and metadata.
        """
        os.makedirs(directory, exist_ok=True)

        index_path = os.path.join(directory, "index.faiss")
        metadata_path = os.path.join(directory, "metadata.pkl")

        faiss.write_index(self.index, index_path)

        with open(metadata_path, "wb") as f:
            pickle.dump(self.metadata, f)

        logger.info(f"Index and metadata saved to {directory}")

    def load(self, directory: str) -> None:
        """
        Load FAISS index and metadata from disk.
        """

        index_path = os.path.join(directory, "index.faiss")
        metadata_path = os.path.join(directory, "metadata.pkl")

        if not os.path.exists(index_path) or not os.path.exists(metadata_path):
            raise FileNotFoundError(
                "Index or metadata file not found."
            )

        self.index = faiss.read_index(index_path)

        with open(metadata_path, "rb") as f:
            self.metadata = pickle.load(f)

        if self.index.ntotal != len(self.metadata):
            raise ValueError(
                "Index and metadata length mismatch after loading."
            )

        if self.index.d != self.dimension:
            raise ValueError(
                f"Loaded index dimension {self.index.d} "
                f"does not match expected {self.dimension}"
            )

        logger.info(
            f"Loaded FAISS index with {self.index.ntotal} vectors."
        )