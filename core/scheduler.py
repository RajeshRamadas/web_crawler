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
