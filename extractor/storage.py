"""
Storage module.

This file contains all the abstractions needed to store the crawled data in a
data source (e.g. AWS S3, Algolia, or Firebase Firestore).
"""

from abc import ABC, abstractmethod


class GenerationRepository(ABC):
    """
    Repository used to store generations from a particular data source.
    """

    @abstractmethod
    def store_generation(self, generation):
        "Store an instance of a generation in a data source (e.g. Algolia)."

        pass
