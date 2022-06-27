"""
In-memory mock implementation of the `storage` abstraction.
"""

from extractor.storage import GenerationRepository


class MockGenerationRepository(GenerationRepository):
    """
    Repository instance used for testing.
    """

    def __init__(self):
        self.items = []

    def store_generation(self, generation):
        """
        Store a generation in memory.
        """
        super().store_generation(generation)

        self.items.append(generation)

        return self.items
