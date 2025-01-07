import unittest
from frontier import Frontier

class TestFrontier(unittest.TestCase):
    def test_add_url(self):
        frontier = Frontier()
        frontier.add_url('https://example.com')
        self.assertEqual(frontier.size(), 1)

    def test_duplicate_url(self):
        frontier = Frontier()
        frontier.add_url('https://example.com')
        frontier.add_url('https://example.com')
        self.assertEqual(frontier.size(), 1)


if __name__ == "__main__":
    unittest.main()
