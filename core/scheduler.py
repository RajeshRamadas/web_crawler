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
import time
from urllib.parse import urlparse, quote
from downloader import Downloader
from frontier import Frontier
from parser import Parser
from robots_handler import RobotsHandler
from db.storage import Storage
import argparse
import warnings
from urllib3.exceptions import InsecureRequestWarning

# Suppress SSL warnings (not recommended for production environments)
warnings.simplefilter('ignore', InsecureRequestWarning)

class Scheduler:
    def __init__(self, seed_urls, max_threads=5, db_path=None, storage_dir=None):
        self.downloader = Downloader(verify_ssl=False)  # Disable SSL verification (not for production)
        self.frontier = Frontier()
        self.robots_handler = RobotsHandler()
        self.max_threads = max_threads
        self.lock = threading.Lock()

        # Set up timestamped storage directory
        self.timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        self.storage_dir = storage_dir or os.path.join("crawled", self.timestamp)
        os.makedirs(self.storage_dir, exist_ok=True)

        # Set up database path
        self.db_path = db_path or os.path.join(self.storage_dir, "crawled_data.db")
        self.storage = Storage(db_path=self.db_path, storage_dir=self.storage_dir)

        # Initialize frontier with seed URLs
        for url in seed_urls:
            self.frontier.add_url(url)

    def crawl(self):
        threads = []
        for _ in range(self.max_threads):
            t = threading.Thread(target=self.worker)
            t.start()
            threads.append(t)

        # Wait for all threads to finish
        for t in threads:
            t.join()

    def worker(self):
        while True:
            # Get the next URL to crawl
            with self.lock:
                next_url = self.frontier.get_next_url()

            if not next_url:
                break  # Exit if no URLs are left

            if not self.robots_handler.is_allowed(next_url):
                print(f"Blocked by robots.txt: {next_url}")
                continue

            print(f"Fetching: {next_url}")
            try:
                html = self.downloader.fetch(next_url)
                if html:
                    parser = Parser(next_url)
                    links, content, structured_data = parser.parse(html)

                    # Save content and structured data to storage
                    metadata = {"structured_data": structured_data}
                    self.storage.save_content(next_url, content, metadata)

                    # Add new links to the frontier
                    with self.lock:
                        for link in links:
                            self.frontier.add_url(link)

            except Exception as e:
                print(f"Error while processing {next_url}: {e}")

    def save_content(self, url, content):
        # Generate a safe filename from the URL
        parsed_url = urlparse(url)
        sanitized_path = parsed_url.netloc + parsed_url.path.replace("/", "_")
        if parsed_url.query:
            sanitized_path += "_" + quote(parsed_url.query, safe="_")

        filename = f"{sanitized_path}.txt"
        filepath = os.path.join(self.storage_dir, filename)

        try:
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(content)
            print(f"Saved content: {filepath}")
        except Exception as e:
            print(f"Error saving content for {url}: {e}")

if __name__ == "__main__":
    seed_urls = ["https://www.livemint.com"]
    scheduler = Scheduler(seed_urls, max_threads=1)
    start_time = time.time()
    scheduler.crawl()
    print(f"Crawling completed in {time.time() - start_time:.2f} seconds.")


    # parser = argparse.ArgumentParser(description="Web Crawler Scheduler")
    # parser.add_argument("--seed_urls", nargs="+", required=True, help="List of seed URLs to start crawling")
    # parser.add_argument("--max_threads", type=int, default=5, help="Maximum number of threads for crawling")
    # parser.add_argument("--db_path", type=str, help="Path to the database file")
    # parser.add_argument("--storage_dir", type=str, help="Directory to store crawled content")
    # args = parser.parse_args()
    #
    # scheduler = Scheduler(seed_urls=args.seed_urls, max_threads=args.max_threads, db_path=args.db_path, storage_dir=args.storage_dir)
    #
    # start_time = time.time()
    # scheduler.crawl()
    # print(f"Crawling completed in {time.time() - start_time:.2f} seconds.")
