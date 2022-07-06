"""
Implementation of the `crawler` abstraction using Algolia.
"""
import logging
import re

from .crawler import Crawler

import praw


class SubredditCrawler(Crawler):
    def __init__(self, subreddit: str, **kwargs):
        self._reddit_client = praw.Reddit(
            client_id=kwargs["client_id"],
            client_secret=kwargs["client_secret"],
            user_agent=kwargs["user_agent"],
            username=kwargs["reddit_username"],
            password=kwargs["reddit_password"],
        )
        self._subreddit = self._reddit_client.subreddit(subreddit)

    def crawl(self):
        openai_ids = set()

        # Crawl OpenAI DALL-E links from dalle2 subreddit
        # See: https://praw.readthedocs.io/en/stable/code_overview/models/subreddit.html#praw.models.Subreddit.search
        for submission in self._subreddit.search("*", sort="new", time_filter="day"):
            print(f"scraping ({submission})...")
            openai_links = set()

            url = submission.url
            if "labs.openai.com/s" in url:
                openai_links.add(url)

            # Traverse the Comment Tree so that the list contains only `Comment`
            # instances.  Use `limit = None` so that all the `MoreComment` instances
            # are processed.
            comment_tree = submission.comments
            comment_tree.replace_more(limit=None)
            comments = comment_tree.list()
            comments_with_links = [c for c in comments if "labs.openai.com/s" in c.body]
            for comment in comments_with_links:
                for link in re.findall(r"(https?://[^\s]+)", comment.body):
                    openai_links.add(link)

            # Parse the IDs from the links
            for link in openai_links:
                try:
                    openai_id = re.findall(r"s\/(\w+)", link)[0]
                except Exception as e:
                    logging.error(
                        f"ERROR: could not parse link: {link}\nError type: {e}"
                    )
                    continue
                else:
                    openai_ids.add(openai_id)

        return list(openai_ids)
