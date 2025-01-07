import unittest
from robots_handler import RobotsHandler

class TestRobotsHandler(unittest.TestCase):
    def setUp(self):
        self.robots_handler = RobotsHandler()

    def test_parse_allow(self):
        robots_txt = "User-agent: *\nAllow: /"
        self.robots_handler.parse("https://example.com", robots_txt)
        self.assertTrue(self.robots_handler.can_fetch("https://example.com/resource"))

    def test_parse_disallow(self):
        robots_txt = "User-agent: *\nDisallow: /private"
        self.robots_handler.parse("https://example.com", robots_txt)
        self.assertFalse(self.robots_handler.can_fetch("https://example.com/private/data"))

if __name__ == "__main__":
    unittest.main()
