import unittest
from parser import Parser

class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = Parser("https://example.com")
        self.sample_html = '''
        <html>
            <body>
                <p>This is a sample paragraph.</p>
                <a href="/about">About Us</a>
                <a href="/contact">Contact</a>
            </body>
        </html>
        '''

    def test_extract_links(self):
        links, _ = self.parser.parse(self.sample_html)
        expected_links = ["https://example.com/about", "https://example.com/contact"]
        self.assertEqual(links, expected_links)

    def test_extract_content(self):
        _, content = self.parser.parse(self.sample_html)
        expected_content = "This is a sample paragraph."
        self.assertEqual(content, expected_content)

if __name__ == "__main__":
    unittest.main()
