import requests
from urllib.parse import urljoin, urlparse
import time

class RobotsHandler:
    def __init__(self, refresh_interval=3600):
        self.rules = {}
        self.robots_cache = {}
        self.cache_timestamps = {}
        self.refresh_interval = refresh_interval  # Interval in seconds to refresh robots.txt

    def fetch_and_parse(self, base_url):
        domain = f"{urlparse(base_url).scheme}://{urlparse(base_url).netloc}"
        robots_url = urljoin(domain, '/robots.txt')

        # Check if we need to refresh the robots.txt
        current_time = time.time()
        if domain in self.robots_cache and (current_time - self.cache_timestamps[domain] < self.refresh_interval):
            # Use cached rules if still fresh
            return

        try:
            response = requests.get(robots_url, timeout=5, stream=True)
            if response.status_code == 200:
                # Limit size to prevent overly large robots.txt issues
                if int(response.headers.get('Content-Length', 0)) > 1_000_000:  # 1 MB limit
                    print(f"Skipping large robots.txt for {domain}")
                    robots_text = ""
                else:
                    robots_text = response.text
            else:
                robots_text = ""
        except requests.RequestException:
            robots_text = ""

        # Cache robots.txt and update timestamp
        self.robots_cache[domain] = robots_text
        self.cache_timestamps[domain] = current_time
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

        # Fetch and parse robots.txt if not already done
        if domain not in self.rules:
            self.fetch_and_parse(domain)

        # If no rules are found, allow by default
        if domain not in self.rules:
            return True

        # Check for specific user-agent or fallback to '*'
        user_rules = self.rules[domain].get(user_agent) or self.rules[domain].get('*') or []

        for rule in user_rules:
            if self.match_rule(path, rule):
                return False
        return True

    @staticmethod
    def match_rule(path, rule):
        """
        Match a rule against a path with support for '*' and '$' wildcards.
        """
        if '*' in rule or '$' in rule:
            # Replace '*' with regex .* and '$' with end-of-string anchor
            import re
            regex_rule = rule.replace('*', '.*').replace('$', r'\Z')
            return re.match(regex_rule, path) is not None
        return path.startswith(rule)


# if __name__ == "__main__":
#     handler = RobotsHandler(refresh_interval=3600)
#     handler.fetch_and_parse('https://www.livemint.com')
#
#     test_urls = [
#         'https://www.livemint.com/topic/davos-2023',
#         'https://www.livemint.com/about',
#         'https://www.livemint.com/contact'
#     ]
#
#     for test_url in test_urls:
#         print(f"Access to {test_url}: {'Allowed' if handler.is_allowed(test_url) else 'Blocked'}")
