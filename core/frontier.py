"""
Hybrid Queueing (Priority + FIFO):

URLs are added to both a PriorityQueue for critical pages and a deque for fallback crawling.
Critical URLs are processed first, while less important URLs wait in the standard queue.
Domain-Based Throttling:

Tracks the last crawl time for each domain and enforces a delay to prevent overwhelming servers.
If the delay hasn't elapsed, the crawler waits before accessing URLs from the same domain.
Deduplication:

The system ensures that URLs are only added once to avoid redundant crawling.
Priority Management:

Critical URLs (e.g., homepage, login pages) can be assigned higher priority (priority=1), while less important URLs get lower values (priority=2).
"""
from collections import deque
from queue import PriorityQueue
from urllib.parse import urlparse
import time


class Frontier:
    def __init__(self):
        self.priority_queue = PriorityQueue()  # For prioritization
        self.standard_queue = deque()  # For regular FIFO queuing
        self.visited = set()  # Deduplication
        self.domain_delay = {}  # Throttling per domain
        self.delay_time = 2  # Domain delay in seconds

    def add_url(self, url, priority=1):
        parsed_url = urlparse(url)

        if parsed_url.netloc and not self.is_visited(url):
            if priority == 1:
                self.priority_queue.put((priority, url))  # High-priority URLs
            else:
                self.standard_queue.append(url)  # Regular URLs
            self.visited.add(url)  # Mark URL as visited to avoid duplicates

    def get_next_url(self):
        # Process priority URLs first
        if not self.priority_queue.empty():
            _, url = self.priority_queue.get()
        elif self.standard_queue:
            url = self.standard_queue.popleft()
        else:
            return None

        domain = urlparse(url).netloc
        if domain in self.domain_delay:
            # Check for domain-specific delay and wait if necessary
            time_diff = time.time() - self.domain_delay[domain]
            if time_diff < self.delay_time:
                time.sleep(self.delay_time - time_diff)

        # Update last crawl time for the domain
        self.domain_delay[domain] = time.time()
        return url

    def is_visited(self, url):
        return url in self.visited

    def size(self):
        return len(self.standard_queue) + self.priority_queue.qsize()


if __name__ == "__main__":
    frontier = Frontier()

    # Seed URLs
    seed_urls = [
        ('https://www.livemint.com/', 1),
        ('https://www.livemint.com/companies', 2),
        ('https://www.livemint.com/news', 1),
        ('https://www.livemint.com/market', 1)
    ]

    # Add URLs with priority
    for url, priority in seed_urls:
        frontier.add_url(url, priority)

    # Crawl in order of priority
    while frontier.size() > 0:
        next_url = frontier.get_next_url()
        print(f"Crawling: {next_url}")
