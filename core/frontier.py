from collections import deque
from urllib.parse import urlparse

class Frontier:
    def __init__(self):
        self.queue = deque()
        self.seen_urls = set()

    def add_url(self, url):
        parsed_url = urlparse(url)
        if parsed_url.netloc and url not in self.seen_urls:
            self.queue.append(url)
            self.seen_urls.add(url)

    def get_next_url(self):
        if self.queue:
            return self.queue.popleft()
        return None

    def size(self):
        return len(self.queue)

if __name__ == "__main__":
    frontier = Frontier()
    seed_urls = [
        'https://example.com',
        'https://example.com/about',
        'https://example.com/contact'
    ]

    for url in seed_urls:
        frontier.add_url(url)

    while frontier.size() > 0:
        next_url = frontier.get_next_url()
        print(f"Crawling: {next_url}")
