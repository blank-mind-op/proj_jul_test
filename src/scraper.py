from bs4 import BeautifulSoup

class BaseScraper:
    def __init__(self, content):
        self.soup = BeautifulSoup(content, "lxml")

    def scrape(self):
        raise NotImplementedError("Each scraper must implement its own scrape method.")

class ParagraphScraper(BaseScraper):
    def __init__(self, content, keyword):
        super().__init__(content)
        self.keyword = keyword

    def scrape(self):
        """
        Scrapes a page for paragraphs containing a keyword.

        Returns:
            list: A list of paragraphs containing the keyword.
        """
        paragraphs = []
        for p in self.soup.find_all("p"):
            if self.keyword.lower() in p.get_text().lower():
                paragraphs.append(p.get_text())
        return paragraphs

import subprocess
import json

def sherlock_scrape(username):
    """
    Uses sherlock to find social media accounts for a given username.

    Args:
        username (str): The username to search for.

    Returns:
        dict: A dictionary of social media accounts found by sherlock.
    """
    try:
        command = ["sherlock", "--json", "-", username]
        result = subprocess.run(command, capture_output=True, text=True)
        # Sherlock outputs the JSON to stderr
        if result.stderr:
            # The output may contain multiple JSON objects, one per line.
            # We'll take the last one, which is the summary.
            lines = result.stderr.strip().split('\n')
            for line in reversed(lines):
                try:
                    return json.loads(line)
                except json.JSONDecodeError:
                    continue
        return {}
    except FileNotFoundError:
        print("Sherlock not found. Please make sure it is installed and in your PATH.")
        return {}
