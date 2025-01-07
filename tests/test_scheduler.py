import unittest
from unittest.mock import MagicMock
from scheduler import Scheduler
from downloader import Downloader
from parser import Parser
from frontier import Frontier


class TestScheduler(unittest.TestCase):
    def setUp(self):
        # Mock dependencies
        self.downloader = MagicMock(spec=Downloader)
        self.parser = MagicMock(spec=Parser)
        self.frontier = MagicMock(spec=Frontier)

        # Initialize scheduler with mocks
        self.scheduler = Scheduler(self.downloader, self.parser, self.frontier)

        # Sample data
        self.sample_html = '''
        <html>
            <body>
                <p>Welcome to the crawler test.</p>
                <a href="/next">Next Page</a>
            </body>
        </html>
        '''
        self.frontier.get_next_url.return_value = "https://example.com"
        self.downloader.fetch.return_value.text = self.sample_html
        self.parser.parse.return_value = (["https://example.com/next"], "Welcome to the crawler test.")

    def test_crawl_page(self):
        # Execute crawling logic
        self.scheduler.crawl()

        # Assertions
        self.frontier.get_next_url.assert_called_once()
        self.downloader.fetch.assert_called_once_with("https://example.com")
        self.parser.parse.assert_called_once_with(self.sample_html)

        # Ensure extracted links are added to the frontier
        self.frontier.add_url.assert_called_once_with("https://example.com/next")

    def test_no_url_in_frontier(self):
        self.frontier.get_next_url.return_value = None

        # Crawl when no URLs are left
        self.scheduler.crawl()

        # Ensure no download happens if no URLs exist
        self.downloader.fetch.assert_not_called()
        self.parser.parse.assert_not_called()


if __name__ == "__main__":
    unittest.main()
