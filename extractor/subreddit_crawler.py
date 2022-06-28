"""
Implementation of the `crawler` abstraction using Algolia.
"""
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
        # Finds the submissions from the last hour
        for submission in self._subreddit.search("*", sort="new", time_filter="hour"):
            openai_links = set()

            url = submission.url
            permalink = submission.permalink
            comments = submission.comments.list()

            if "labs.openai" in url:
                openai_links.add(url)

            for comment in comments:
                links = [
                    link
                    for link in re.findall(r"(https?://[^\s]+)", comment.body)
                    if "labs.openai.com" in link
                ]
                for link in links:
                    openai_links.add(link)

            for link in openai_links:
                openai_id = re.findall(r"s\/(\w+)", link)[0]
                openai_ids.add(openai_id)

        return list(openai_ids)
