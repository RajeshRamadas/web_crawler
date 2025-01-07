import unittest
from downloader import Downloader

class TestDownloader(unittest.TestCase):
    def setUp(self):
        self.downloader = Downloader(user_agent="TestBot")

    def test_download_success(self):
        url = "https://example.com"
        response = self.downloader.fetch(url)
        self.assertEqual(response.status_code, 200)

    def test_download_invalid_url(self):
        url = "invalid-url"
        with self.assertRaises(Exception):
            self.downloader.fetch(url)

if __name__ == "__main__":
    unittest.main()
