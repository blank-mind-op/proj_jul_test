import requests

def get_html(url):
    """
    Fetches the HTML content of a given URL.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the URL, or None if the request fails.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_links(base_url, html):
    """
    Parses HTML content and extracts all links.

    Args:
        base_url (str): The base URL to resolve relative links.
        html (str): The HTML content to parse.

    Returns:
        list: A list of absolute URLs found on the page.
    """
    soup = BeautifulSoup(html, "lxml")
    links = []
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        absolute_url = urljoin(base_url, href)
        links.append(absolute_url)
    return links

def crawl(start_url, max_depth=2):
    """
    Crawls a website starting from a given URL up to a maximum depth.

    Args:
        start_url (str): The URL to start crawling from.
        max_depth (int): The maximum depth to crawl.

    Returns:
        set: A set of visited URLs.
    """
    visited = set()
    to_visit = [(start_url, 0)]

    while to_visit:
        url, depth = to_visit.pop(0)

        if url in visited or depth > max_depth:
            continue

        print(f"Crawling: {url}")
        html = get_html(url)

        if html:
            visited.add(url)
            links = get_links(url, html)
            for link in links:
                if link not in visited:
                    to_visit.append((link, depth + 1))

    return visited
