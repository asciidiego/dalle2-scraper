from mock_storage import MockGenerationRepository


def test_storing_item():
    item = {
        "image_path": "",
        "generation_prompt": "",
        "author_name": "",
        "thumbnail_path": "",
    }
    generation_repo = MockGenerationRepository()

    result = generation_repo.store_generation(item)

    assert len(result) == 1
