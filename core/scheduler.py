"""
Key Improvements and Merging Details:
Parallel Crawling:

Uses threading to run multiple workers concurrently (max_threads).
Each worker fetches URLs from the frontier and processes them independently.
Thread Safety with Locks:

The lock ensures that frontier.get_next_url and frontier.add_url are thread-safe.
This prevents race conditions when multiple threads modify the queue.
Graceful Shutdown:

Each worker exits when no URLs remain in the frontier (get_next_url returns None).
Threads terminate gracefully without forcing a shutdown.
Adaptive Crawling with Robots.txt:

Before fetching a URL, the worker checks if crawling is allowed by robots.txt (is_allowed).
This prevents unnecessary requests to disallowed paths.
Content Persistence:

Each page is saved as a .txt file under the crawled directory, using a sanitized filename based on the URL.
Performance Reporting:

Tracks total crawling time to monitor performance.

Testing and Customization:
Adjust max_threads based on network speed and system performance.
Add more URLs to seed_urls to test the scalability.
Extend RobotsHandler to refresh cached robots.txt periodically for long-running crawls.
"""

import threading
import os
from urllib.parse import urlparse, quote
from downloader import Downloader
from frontier import Frontier
from parser import Parser
from robots_handler import RobotsHandler
import time


class Scheduler:
    def __init__(self, seed_urls, max_threads=5):
        self.downloader = Downloader()
        self.frontier = Frontier()
        self.robots_handler = RobotsHandler()
        self.max_threads = max_threads
        self.lock = threading.Lock()

        # Initialize with seed URLs
        for url in seed_urls:
            self.frontier.add_url(url)

        # Ensure output directory exists
        if not os.path.exists("crawled"):
            os.makedirs("crawled")

    def crawl(self):
        threads = []
        for _ in range(self.max_threads):
            t = threading.Thread(target=self.worker)
            t.start()
            threads.append(t)

        # Wait for all threads to complete
        for t in threads:
            t.join()

    def worker(self):
        while True:
            # Fetch the next URL to crawl
            with self.lock:
                next_url = self.frontier.get_next_url()

            if not next_url:
                break  # Exit if no URLs left

            if not self.robots_handler.is_allowed(next_url):
                print(f"Blocked by robots.txt: {next_url}")
                continue

            print(f"Fetching: {next_url}")
            try:
                html = self.downloader.fetch(next_url)
                if html:
                    parser = Parser(next_url)
                    result = parser.parse(html)

                    # Handle parse result
                    if len(result) >= 2:
                        links, content = result[:2]
                        self.save_content(next_url, content)

                        # Add new links to the frontier
                        with self.lock:
                            for link in links:
                                self.frontier.add_url(link)
                    else:
                        print(f"Parser returned unexpected result: {result}")

            except Exception as e:
                print(f"Error while processing {next_url}: {e}")

    def save_content(self, url, content):
        # Generate a safe filename from the URL
        parsed_url = urlparse(url)
        sanitized_path = parsed_url.netloc + parsed_url.path.replace("/", "_")
        if parsed_url.query:
            sanitized_path += "_" + quote(parsed_url.query, safe="_")

        filename = f"{sanitized_path}.txt"
        filepath = os.path.join("crawled", filename)

        try:
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(content)
            print(f"Saved content: {filepath}")
        except Exception as e:
            print(f"Error saving content for {url}: {e}")


if __name__ == "__main__":
    seed_urls = ["https://www.livemint.com/"]
    scheduler = Scheduler(seed_urls, max_threads=3)
    start_time = time.time()
    scheduler.crawl()
    print(f"Crawling completed in {time.time() - start_time:.2f} seconds.")
