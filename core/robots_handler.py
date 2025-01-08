import requests
from urllib.parse import urljoin, urlparse

class RobotsHandler:
    def __init__(self):
        self.rules = {}
        self.robots_cache = {}

    def fetch_and_parse(self, base_url):
        domain = f"{urlparse(base_url).scheme}://{urlparse(base_url).netloc}"
        robots_url = urljoin(domain, '/robots.txt')

        if domain in self.robots_cache:
            # Use cached rules if available
            self.parse_rules(domain, self.robots_cache[domain])
            return

        try:
            response = requests.get(robots_url, timeout=5)
            if response.status_code == 200:
                robots_text = response.text
            else:
                robots_text = ""
        except requests.RequestException:
            robots_text = ""

        # Cache robots.txt even if empty (to avoid repeated fetches)
        self.robots_cache[domain] = robots_text
        self.parse_rules(domain, robots_text)

    def parse_rules(self, domain, robots_text):
        current_user_agent = None
        self.rules[domain] = {}

        for line in robots_text.splitlines():
            line = line.strip()
            if line.startswith('#') or line == '':
                continue

            if line.lower().startswith('user-agent:'):
                current_user_agent = line.split(':', 1)[1].strip()
            elif line.lower().startswith('disallow:') and current_user_agent:
                disallow_path = line.split(':', 1)[1].strip()
                if current_user_agent not in self.rules[domain]:
                    self.rules[domain][current_user_agent] = []
                self.rules[domain][current_user_agent].append(disallow_path)

    def is_allowed(self, url, user_agent='*'):
        parsed = urlparse(url)
        domain = f"{parsed.scheme}://{parsed.netloc}"
        path = parsed.path or '/'

        # If no rules are found, allow by default
        if domain not in self.rules:
            return True

        # Check for specific user-agent or fallback to '*'
        user_rules = self.rules[domain].get(user_agent) or self.rules[domain].get('*') or []
        for rule in user_rules:
            if path.startswith(rule):
                return False
        return True


if __name__ == "__main__":
    handler = RobotsHandler()
    handler.fetch_and_parse('https://www.livemint.com')

    test_urls = [
        'https://www.livemint.com/topic/davos-2023',
        'https://www.livemint.com/about',
        'https://www.livemint.com/contact'
    ]

    for test_url in test_urls:
        print(f"Access to {test_url}: {'Allowed' if handler.is_allowed(test_url) else 'Blocked'}")
