from mock_storage import MockGenerationRepository


def test_storing_item():
    item = {}
    generation_repo = MockGenerationRepository()

    result = generation_repo.store_generation(item)

    assert len(result) == 1
