import requests
from urllib.parse import urljoin
import time
import random
from bs4 import BeautifulSoup

class Downloader:
    def __init__(self, user_agents=None, delay=1, timeout=10, retries=3):
        self.user_agents = user_agents or [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        ]
        self.delay = delay
        self.timeout = timeout
        self.retries = retries

    def fetch(self, url):
        headers = {'User-Agent': random.choice(self.user_agents)}
        for attempt in range(self.retries):
            try:
                response = requests.get(url, headers=headers, timeout=self.timeout)
                response.raise_for_status()
                time.sleep(self.delay)
                return response.text
            except requests.exceptions.RequestException as e:
                print(f"Attempt {attempt + 1} failed for {url}: {e}")
                time.sleep(self.delay)
        return None

    def fetch_links(self, url, link_selector):
        html = self.fetch(url)
        if not html:
            return []
        soup = BeautifulSoup(html, 'html.parser')
        links = [urljoin(url, a['href']) for a in soup.select(link_selector) if 'href' in a.attrs]
        return links

if __name__ == "__main__":
    downloader = Downloader()
    start_url = 'https://www.livemint.com/companies/news/tata-electronics-proposal-to-acquire-majority-stake-in-pegatron-india-gets-cci-nod-11736259785701.html'
    html_content = downloader.fetch(start_url)
    print(html_content)
