import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}

def is_internal_link(link, base_url):
    base_netloc = urlparse(base_url).netloc
    parsed_link = urlparse(link)
    return parsed_link.netloc == '' or parsed_link.netloc == base_netloc

def fetch_page_data(url, base_url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if not response.ok:
            return {
                'url': url,
                'error': f"{response.status_code} {response.reason}",
                'content': '',
                'links': [],
                'internal_links': [],
                'images': [],
            }

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract all <a> links
        links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True)]

        # Filter internal links
        internal_links = list(set(
            link for link in links if is_internal_link(link, base_url)
        ))

        # Extract all <img> links
        images = [urljoin(url, img['src']) for img in soup.find_all('img', src=True)]

        return {
            'url': url,
            'content': soup.get_text(separator=' ', strip=True),
            'links': links,
            'internal_links': internal_links,
            'images': images,
        }
    except Exception as e:
        return {
            'url': url,
            'error': str(e),
            'content': '',
            'links': [],
            'internal_links': [],
            'images': [],
        }

def crawl_website(start_url, max_pages=20):
    visited = set()
    to_visit = [start_url]
    results = []

    while to_visit and len(visited) < max_pages:
        current_url = to_visit.pop(0)
        if current_url in visited:
            continue

        data = fetch_page_data(current_url, start_url)
        results.append(data)

        if 'internal_links' in data:
            for link in data['internal_links']:
                if link not in visited and link not in to_visit:
                    to_visit.append(link)

        visited.add(current_url)

    return results
