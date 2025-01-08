"""
# Robust link extraction to handle malformed URLs.
# Content extraction refinement to filter irrelevant data (e.g., ads, scripts).
# Structured data extraction with schema detection.
"""
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

class Parser:
    def __init__(self, base_url):
        self.base_url = base_url

    def parse(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        links = self.extract_links(soup)
        content = self.extract_content(soup)
        structured_data = self.extract_structured_data(soup)
        return links, content, structured_data

    def extract_links(self, soup):
        links = set()  # Use set to avoid duplicates
        for a_tag in soup.find_all('a', href=True):
            full_url = urljoin(self.base_url, a_tag['href'])
            if self.is_valid_url(full_url):
                links.add(full_url)
        return list(links)

    def extract_content(self, soup):
        # Remove script, style, and ad-related tags
        for tag in soup(['script', 'style', 'iframe', 'noscript']):
            tag.decompose()

        paragraphs = soup.find_all('p')
        content = '\n'.join([p.get_text(strip=True) for p in paragraphs])
        return content.strip()

    def extract_structured_data(self, soup):
        structured_data = {}
        # Extract JSON-LD structured data
        json_ld_tags = soup.find_all('script', type="application/ld+json")
        structured_data['json_ld'] = [tag.string for tag in json_ld_tags if tag.string]

        # Extract meta tags for keywords or descriptions
        meta_tags = {meta['name']: meta['content'] for meta in soup.find_all('meta', attrs={'name': True, 'content': True})}
        structured_data['meta'] = meta_tags

        return structured_data

    def is_valid_url(self, url):
        parsed = urlparse(url)
        return bool(parsed.netloc) and parsed.scheme in ['http', 'https']

if __name__ == "__main__":
    sample_html = '''
    <html>
        <head>
            <meta name="description" content="Sample page for testing.">
            <script>console.log("This should not be extracted.")</script>
        </head>
        <body>
            <p>This is a sample paragraph.</p>
            <a href="/about">About Us</a>
            <a href="https://malformed url">Malformed Link</a>
            <a href="/contact">Contact</a>
        </body>
    </html>
    '''
    parser = Parser("https://www.livemint.com/")
    links, content, structured_data = parser.parse(sample_html)
    print("Extracted Links:", links)
    print("Extracted Content:", content)
    print("Extracted Structured Data:", structured_data)

