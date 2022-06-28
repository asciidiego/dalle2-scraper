"""
Crawler module.

This module is in charge of crawling links from a particular source (e.g. /r/dalle2).
"""

from abc import ABC, abstractmethod


class Crawler(ABC):
    """
    Abstract crawler class.
    """

    @abstractmethod
    def crawl(self):
        pass
