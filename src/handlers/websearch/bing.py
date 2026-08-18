from .websearch import WebSearchHandler
from ...handlers import ExtraSettings, ErrorSeverity
from ...utility.website_scraper import WebsiteScraper

BING_SEARCH_URL = "https://www.bing.com/search"


class BingHandler(WebSearchHandler):
    key = "bing"

    def get_extra_settings(self) -> list:
        return [
            ExtraSettings.EntrySetting("lang", "Language", "Language for the search results", "en"),
            ExtraSettings.ScaleSetting("results", "Results", "Number of results to consider", 3, 1, 10, 0),
            ExtraSettings.ToggleSetting("streaming", "Show search progress", "Show search progress", True),
        ]

    def supports_streaming_query(self) -> bool:
        return self.get_setting("streaming")

    def query(self, keywords: str, max_results: int = None) -> tuple[str, list]:
        return self.query_streaming(keywords, lambda title, link, favicon: None, max_results=max_results)

    def query_streaming(self, keywords: str, add_website, max_results: int = None) -> tuple[str, list]:
        try:
            results = self.get_links(keywords)
        except Exception as e:
            self.throw("Failed to query Bing: " + str(e), ErrorSeverity.WARNING)
            return "No results found", []
        content, urls = self.scrape_websites(results, add_website, max_results=max_results)
        text = "\n\n".join(
            self.format_source(result["title"], result["url"], result["text"][:3000])
            for result in content
        )
        return text, urls

    def get_links(self, query: str) -> list[tuple[str, str]]:
        """Query Bing and return a list of (url, title) tuples from the HTML results page."""
        import requests
        from bs4 import BeautifulSoup

        lang = self.get_setting("lang")
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.0",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
        params = {"q": query, "setlang": lang, "cc": "us", "count": "10"}
        r = requests.get(BING_SEARCH_URL, params=params, headers=headers, timeout=10)
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

    def scrape_websites(self, result_links: list[tuple[str, str]], update, max_results: int = None) -> tuple[list, list]:
        """Fetch and extract the content of each result page, feeding progress back via update."""
        if max_results is None:
            max_results = self.get_setting("results")
        max_results = int(max_results)
        if not result_links:
            return [], []

        urls = []
        extracted_content = []
        processed_count = 0
        for url, initial_title in result_links:
            if processed_count >= max_results:
                break
            article_data = {"url": url, "title": initial_title, "text": ""}
            try:
                article = WebsiteScraper(url)
                article.parse_article()
                update(article.get_title(), url, article.get_favicon())
                text = article.get_text()
                if text:
                    article_data["title"] = article.get_title() or initial_title
                    article_data["text"] = text
                    extracted_content.append(article_data)
                    urls.append(url)
                    processed_count += 1
            except Exception as e:
                print(f"An unexpected error occurred processing {url}: {e}")
        return extracted_content, urls
