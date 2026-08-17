from .bing import BingHandler

BING_INTERNATIONAL_SEARCH_URL = "https://global.bing.com/search"


class BingInternationalHandler(BingHandler):
    key = "bing_international"

    def get_links(self, query: str) -> list[tuple[str, str]]:
        """Query Bing international and return a list of (url, title) tuples from the HTML results page."""
        import requests
        from bs4 import BeautifulSoup

        lang = self.get_setting("lang")
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.0",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
        params = {"q": query, "setlang": lang, "setmkt": "en-WW", "mkt": "en-WW", "count": "10"}
        r = requests.get(BING_INTERNATIONAL_SEARCH_URL, params=params, headers=headers, timeout=10)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")
        results = []
        for item in soup.select("li.b_algo"):
            heading = item.find("h2")
            link = heading.find("a", href=True) if heading is not None else None
            if link is None:
                link = item.find("a", href=True)
            if link is None:
                continue
            url = link.get("href")
            title = link.get_text(strip=True)
            if url and url.startswith("http"):
                results.append((url, title))
        return results
