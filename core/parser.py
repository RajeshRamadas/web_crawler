from bs4 import BeautifulSoup
from urllib.parse import urljoin

class Parser:
    def __init__(self, base_url):
        self.base_url = base_url

    def parse(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        links = self.extract_links(soup)
        content = self.extract_content(soup)
        return links, content

    def extract_links(self, soup):
        links = []
        for a_tag in soup.find_all('a', href=True):
            full_url = urljoin(self.base_url, a_tag['href'])
            links.append(full_url)
        return links

    def extract_content(self, soup):
        paragraphs = soup.find_all('p')
        content = '\n'.join([p.get_text() for p in paragraphs])
        return content

if __name__ == "__main__":
    sample_html = '''
    <html>
        <body>
            <p>This is a sample paragraph.</p>
            <a href="/about">About Us</a>
            <a href="/contact">Contact</a>
        </body>
    </html>
    '''
    parser = Parser("https://example.com")
    links, content = parser.parse(sample_html)
    print("Extracted Links:", links)
    print("Extracted Content:", content)
