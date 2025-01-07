
from downloader import Downloader
from frontier import Frontier
from parser import Parser

class Scheduler:
    def __init__(self, seed_urls):
        self.downloader = Downloader()
        self.frontier = Frontier()
        self.seed_urls = seed_urls

        for url in self.seed_urls:
            self.frontier.add_url(url)

    def run(self):
        while self.frontier.size() > 0:
            next_url = self.frontier.get_next_url()
            print(f"Fetching: {next_url}")
            html = self.downloader.fetch(next_url)
            if html:
                parser = Parser(next_url)
                links, content = parser.parse(html)
                self.save_content(next_url, content)
                for link in links:
                    self.frontier.add_url(link)

    def save_content(self, url, content):
        filename = url.replace("https://", "").replace("http://", "").replace("/", "_") + ".txt"
        with open(f"crawled/{filename}", "w", encoding="utf-8") as file:
            file.write(content)

if __name__ == "__main__":
    seed_urls = ["https://example.com"]
    scheduler = Scheduler(seed_urls)
    scheduler.run()


"""

# Parallel crawling using threading or asyncio.
# Graceful shutdown to handle interruptions.
# Adaptive scheduling to adjust crawling speed dynamically.
import threading

class Scheduler:
    def __init__(self, downloader, parser, frontier, robots_handler):
        self.downloader = downloader
        self.parser = parser
        self.frontier = frontier
        self.robots_handler = robots_handler

    def crawl(self, max_threads=5):
        threads = []
        for _ in range(max_threads):
            t = threading.Thread(target=self.worker)
            t.start()
            threads.append(t)
        for t in threads:
            t.join()

    def worker(self):
        while True:
            url = self.frontier.get_next_url()
            if not url:
                break
            if self.robots_handler.can_fetch(url):
                try:
                    response = self.downloader.fetch(url)
                    links, content = self.parser.parse(response.text)
                    for link in links:
                        self.frontier.add_url(link)
                    print(f"Crawled: {url}")
                except Exception as e:
                    print(f"Failed to crawl {url}: {e}")

"""