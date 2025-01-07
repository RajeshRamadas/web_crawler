import requests
from urllib.parse import urljoin, urlparse

class RobotsHandler:
    def __init__(self):
        self.rules = {}

    def fetch_and_parse(self, base_url):
        robots_url = urljoin(base_url, '/robots.txt')
        try:
            response = requests.get(robots_url, timeout=5)
            if response.status_code == 200:
                self.parse_rules(base_url, response.text)
        except requests.RequestException as e:
            print(f"Failed to fetch robots.txt for {base_url}: {e}")

    def parse_rules(self, base_url, robots_text):
        current_user_agent = None
        parsed_url = urlparse(base_url).netloc
        self.rules[parsed_url] = {}

        for line in robots_text.splitlines():
            line = line.strip()
            if line.startswith('#') or line == '':
                continue
            if line.lower().startswith('user-agent:'):
                current_user_agent = line.split(':', 1)[1].strip()
            elif line.lower().startswith('disallow:') and current_user_agent:
                disallow_path = line.split(':', 1)[1].strip()
                if current_user_agent not in self.rules[parsed_url]:
                    self.rules[parsed_url][current_user_agent] = []
                self.rules[parsed_url][current_user_agent].append(disallow_path)

    def is_allowed(self, url, user_agent='*'):
        parsed = urlparse(url)
        netloc = parsed.netloc
        path = parsed.path or '/'

        if netloc not in self.rules:
            return True

        user_rules = self.rules[netloc].get(user_agent) or self.rules[netloc].get('*') or []
        for rule in user_rules:
            if path.startswith(rule):
                return False
        return True

if __name__ == "__main__":
    handler = RobotsHandler()
    handler.fetch_and_parse('https://www.livemint.com/topic/davos-2023')
    test_url = 'https://www.livemint.com/topic/davos-2023'
    print(f"Access to {test_url}: {'Allowed' if handler.is_allowed(test_url) else 'Blocked'}")


"""
# Cache robots.txt for each domain to avoid repeated downloads.
# Graceful fallback if robots.txt is unreachable.
import requests
from urllib.parse import urljoin, urlparse

class RobotsHandler:
    def __init__(self):
        self.robots_cache = {}

    def fetch(self, url):
        domain = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
        robots_url = urljoin(domain, '/robots.txt')
        if domain not in self.robots_cache:
            try:
                response = requests.get(robots_url, timeout=5)
                self.robots_cache[domain] = response.text if response.status_code == 200 else ""
            except requests.exceptions.RequestException:
                self.robots_cache[domain] = ""
        return self.robots_cache[domain]

    def can_fetch(self, url):
        domain = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
        robots_txt = self.robots_cache.get(domain, "")
        if "Disallow" in robots_txt:
            disallowed_paths = [line.split(":")[1].strip() for line in robots_txt.split("\n") if line.startswith("Disallow")]
            for path in disallowed_paths:
                if urlparse(url).path.startswith(path):
                    return False
        return True

"""
