import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
from typing import Set

async def fetch_html(client, url):
    try:
        resp = await client.get(url, timeout=10)
        if resp.status_code == 200 and "text/html" in resp.headers.get("content-type", ""):
            return resp.text
    except:
        return None

async def crawl_website(start_url: str):
    visited: Set[str] = set()
    queue = deque([start_url])
    domain = urlparse(start_url).netloc

    async with httpx.AsyncClient(follow_redirects=True) as client:
        while queue:
            current_url = queue.popleft()
            if current_url in visited:
                continue

            visited.add(current_url)
            html = await fetch_html(client, current_url)
            if not html:
                continue

            soup = BeautifulSoup(html, "html.parser")
            for link_tag in soup.find_all("a", href=True):
                href = link_tag.get("href")
                full_url = urljoin(current_url, href)
                if urlparse(full_url).netloc == domain and full_url not in visited:
                    queue.append(full_url)

    return list(visited)
