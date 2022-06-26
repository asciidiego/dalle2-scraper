import json
import os
from attr import attr

from dotenv import load_dotenv
from algoliasearch.search_client import SearchClient


def create_algolia_generation_storage_fn(app_id, api_key, index):
    """Creates a function that stores dall-e 2 generations.
    
    - `index` is the Algolia index where the items will be stored.
    """

    client = SearchClient.create(app_id=app_id, api_key=api_key)
    algolia_index = client.init_index(index)

    def store_generation(generation_record):
        required_attributes = [
            "image_path",
            "generation_prompt",
            "author_name",
            "thumbnail_path",
        ]
        for attribute in required_attributes:
            assert attribute in generation_record, f"item has no {attribute} attribute."

        algolia_index.save_object(generation_record).wait()

    return store_generation


if __name__ == "__main__":
    load_dotenv()
    store_generation = create_algolia_generation_storage_fn(
        app_id=os.getenv("ALGOLIA_APP_ID"),
        api_key=os.getenv("ALGOLIA_API_KEY"),
        index=os.getenv("ALGOLIA_STORAGE_INDEX"),
    )

    with open("output.jsonl", "r") as f:
        for line in f:
            raw_item = json.loads(line)
            generation_item = {
                "objectID": raw_item["id"],
                "image_path": raw_item["generation"]["image_path"],
                "generation_prompt": raw_item["prompt"]["prompt"]["caption"],
                "author_name": raw_item["user"]["name"],
                "thumbnail_path": raw_item["generation"]["image_path"],
            }
            store_generation(generation_item)
