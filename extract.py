"""
Script to start the dalle2 generations extraction process.
"""

import json
import os
from dotenv import load_dotenv

from extractor.algolia_storage import AlgoliaGenerationRepository


if __name__ == "__main__":
    load_dotenv()

    generation_repository = AlgoliaGenerationRepository(
        app_id=os.getenv("ALGOLIA_APP_ID"),
        api_key=os.getenv("ALGOLIA_API_KEY"),
        generation_index=os.getenv("ALGOLIA_STORAGE_INDEX"),
    )

    # TODO: add reddit crawling module (to crawl OpenAI links from reddit)
    # TODO: add openai scraping (to scrape dalle2 generation information from OpenAI)

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
            generation_repository.store_generation(generation_item)
