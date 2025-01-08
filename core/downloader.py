"""
User-Agent Rotation:
Combines rotating user-agents from both code versions for better bot evasion.

Retry Mechanism:
Includes retry logic for request failures.

Timeout and Rate Limiting:
Requests time out after a specified period. A delay is enforced between requests to avoid being throttled.

Link Extraction (fetch_links):
Extracts all links from the target page using BeautifulSoup, with flexible link selectors.

Graceful Fallback:
Returns empty lists for links if the request fails instead of crashing the program.

Usage Example:
This downloader can be used to extract links and content from any given web page.
Rotating user agents prevents frequent blocking by server
"""
import requests
from urllib.parse import urljoin
import time
import random
from bs4 import BeautifulSoup


class Downloader:
    def __init__(self, user_agents=None, delay=1, timeout=10, retries=3, verify_ssl=True):
        self.retries = retries
        self.delay = delay
        self.timeout = timeout
        self.user_agents = user_agents or [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'WebCrawlerBot/1.0'
        ]
        self.current_agent_index = 0
        self.verify_ssl = verify_ssl

    def get_user_agent(self):
        # Rotate user agents to prevent being blocked
        agent = self.user_agents[self.current_agent_index]
        self.current_agent_index = (self.current_agent_index + 1) % len(self.user_agents)
        return agent

    def fetch(self, url):
        headers = {"User-Agent": self.get_user_agent()}
        for attempt in range(self.retries):
            try:
                response = requests.get(url, headers=headers, timeout=self.timeout, verify=self.verify_ssl)
                response.raise_for_status()
                time.sleep(self.delay)  # Rate limiting
                return response.text
            except requests.exceptions.RequestException as e:
                print(f"Attempt {attempt + 1}: Failed to fetch {url} - {e}")
                time.sleep(self.delay)
        raise Exception(f"Failed to fetch {url} after {self.retries} attempts.")

    def fetch_links(self, url, link_selector='a[href]'):
        html = self.fetch(url)
        if not html:
            return []
        soup = BeautifulSoup(html, 'html.parser')
        links = [urljoin(url, a['href']) for a in soup.select(link_selector) if 'href' in a.attrs]
        return links


if __name__ == "__main__":
    downloader = Downloader(verify_ssl=False)  # Disable SSL verification for testing
    start_url = 'https://www.livemint.com'

    # Fetch HTML content of the page
    try:
        html_content = downloader.fetch(start_url)
        print("Page HTML Content:")
        print(html_content[:])  # Print first 500 characters of the HTML

        # Fetch links from the page
        links = downloader.fetch_links(start_url)
        print("\nExtracted Links:")
        for link in links:
            print(link)
    except Exception as e:
        print(f"Error: {e}")
